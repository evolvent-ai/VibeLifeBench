"""Recurring payment schedules (list / schedule / cancel)."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import parse_date
from ..utils.exceptions import (
    BadAmountError,
    BadArgError,
    PayeeNotFoundError,
    ScheduleNotFoundError,
)
from ..utils.freq import validate_freq
from ..utils.ids import schedule_id as make_schedule_id
from ._posting import fetch_account

logger = logging.getLogger(__name__)

VALID_STATUS = ("active", "paused", "cancelled", "ended")


class RecurringService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- list ------------------------------------------------------------
    def list_recurring(
        self,
        user_id: str,
        status_filter: Optional[str] = None,
    ) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        if status_filter is not None and status_filter not in VALID_STATUS:
            raise BadArgError(f"status_filter must be one of {VALID_STATUS}")

        sql = [
            "SELECT r.schedule_id, r.account_id, r.payee_id, r.amount_minor, "
            "r.freq, r.next_run_date, r.status, p.name AS payee_name "
            "FROM recurring_payments r "
            "LEFT JOIN payees p ON p.payee_id = r.payee_id "
            "WHERE r.user_id = ?"
        ]
        args: List = [user_id]
        if status_filter:
            sql.append("AND r.status = ?")
            args.append(status_filter)
        sql.append("ORDER BY r.next_run_date ASC, r.schedule_id ASC")
        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [
            {
                "schedule_id": r["schedule_id"],
                "account_id": r["account_id"],
                "payee_id": r["payee_id"],
                "payee_name": r["payee_name"],
                "amount_minor": int(r["amount_minor"]),
                "freq": r["freq"],
                "next_run_date": r["next_run_date"],
                "status": r["status"],
            }
            for r in rows
        ]

    # ---- schedule --------------------------------------------------------
    def schedule_recurring(
        self,
        account_id: str,
        payee_id: str,
        amount_minor: int,
        freq: str,
        start_date: str,
        end_date: Optional[str] = None,
    ) -> dict:
        if amount_minor is None or int(amount_minor) <= 0:
            raise BadAmountError("amount_minor must be a positive integer")
        validate_freq(freq)
        sd = parse_date(start_date)
        if end_date:
            ed = parse_date(end_date)
            if ed < sd:
                raise BadArgError("end_date must be on or after start_date")

        acct = fetch_account(self.conn, account_id)
        payee_row = self.conn.execute(
            "SELECT * FROM payees WHERE payee_id = ?", (payee_id,)
        ).fetchone()
        if not payee_row:
            raise PayeeNotFoundError(f"payee not found: {payee_id}")
        if payee_row["user_id"] != acct["user_id"]:
            raise PayeeNotFoundError("payee does not belong to account owner")

        seq = next_counter(self.conn, "schedule_seq")
        new_id = make_schedule_id(seq)
        self.conn.execute(
            """
            INSERT INTO recurring_payments
              (schedule_id, user_id, account_id, payee_id, amount_minor,
               freq, start_date, end_date, next_run_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
            """,
            (
                new_id,
                acct["user_id"],
                account_id,
                payee_id,
                int(amount_minor),
                freq,
                start_date,
                end_date,
                start_date,
            ),
        )
        return {
            "schedule_id": new_id,
            "next_run_date": start_date,
            "amount_minor": int(amount_minor),
            "freq": freq,
            "status": "active",
        }

    # ---- cancel ----------------------------------------------------------
    def cancel_recurring(self, schedule_id: str) -> dict:
        row = self.conn.execute(
            "SELECT * FROM recurring_payments WHERE schedule_id = ?",
            (schedule_id,),
        ).fetchone()
        if not row:
            raise ScheduleNotFoundError(f"schedule not found: {schedule_id}")
        self.conn.execute(
            "UPDATE recurring_payments SET status = 'cancelled' WHERE schedule_id = ?",
            (schedule_id,),
        )
        return {"schedule_id": schedule_id, "status": "cancelled"}
