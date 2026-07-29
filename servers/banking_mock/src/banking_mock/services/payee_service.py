"""Payees + ad-hoc / future-dated payments to a payee."""
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z, parse_date, today_utc
from ..utils.exceptions import (
    BadAmountError,
    BadArgError,
    PayeeNotFoundError,
)
from ..utils.ids import mask_account_no, payee_id as make_payee_id, pending_id as make_pending_id
from ._posting import fetch_account, post_transaction

logger = logging.getLogger(__name__)

VALID_PENDING_STATUSES = {"pending", "posted", "cancelled"}


class PayeeService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- list / add ------------------------------------------------------
    def list_payees(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT payee_id, name, bank_name, account_no_masked, added_at
            FROM payees WHERE user_id = ? ORDER BY added_at ASC, payee_id ASC
            """,
            (user_id,),
        ).fetchall()
        return [
            {
                "payee_id": r["payee_id"],
                "name": r["name"],
                "bank_name": r["bank_name"],
                "account_no_masked": r["account_no_masked"],
                "added_at": r["added_at"],
            }
            for r in rows
        ]

    def list_pending_payments(
        self,
        user_id: str,
        account_id: Optional[str] = None,
        status_filter: Optional[str] = None,
        limit: int = 50,
    ) -> List[dict]:
        """List future-dated one-off payments visible to an account owner."""
        if not user_id:
            raise BadArgError("user_id is required")
        if status_filter is not None and status_filter not in VALID_PENDING_STATUSES:
            raise BadArgError(
                f"status_filter must be one of {sorted(VALID_PENDING_STATUSES)}"
            )
        if limit is None or int(limit) < 1:
            raise BadArgError("limit must be >= 1")
        limit = min(int(limit), 500)

        sql = [
            "SELECT pp.pending_id, pp.account_id, pp.payee_id, p.name AS payee_name, ",
            "pp.amount_minor, pp.memo, pp.scheduled_for, pp.status ",
            "FROM pending_payments pp ",
            "JOIN accounts a ON a.account_id = pp.account_id ",
            "JOIN payees p ON p.payee_id = pp.payee_id ",
            "WHERE a.user_id = ? ",
        ]
        args: List = [user_id]
        if account_id:
            fetch_account(self.conn, account_id)
            sql.append("AND pp.account_id = ? ")
            args.append(account_id)
        if status_filter:
            sql.append("AND pp.status = ? ")
            args.append(status_filter)
        sql.append("ORDER BY pp.scheduled_for ASC, pp.pending_id ASC LIMIT ?")
        args.append(limit)
        rows = self.conn.execute("".join(sql), args).fetchall()
        return [
            {
                "pending_id": row["pending_id"],
                "account_id": row["account_id"],
                "payee_id": row["payee_id"],
                "payee_name": row["payee_name"],
                "amount_minor": int(row["amount_minor"]),
                "memo": row["memo"],
                "scheduled_for": row["scheduled_for"],
                "status": row["status"],
            }
            for row in rows
        ]

    def add_payee(
        self, user_id: str, name: str, account_no: str, bank_name: str
    ) -> dict:
        if not user_id or not name or not account_no or not bank_name:
            raise BadArgError(
                "user_id, name, account_no, bank_name are all required"
            )
        seq = next_counter(self.conn, "payee_seq")
        new_id = make_payee_id(seq)
        masked = mask_account_no(account_no)
        added = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO payees (payee_id, user_id, name, account_no,
                                account_no_masked, bank_name, added_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (new_id, user_id, name, account_no, masked, bank_name, added),
        )
        return {
            "payee_id": new_id,
            "name": name,
            "bank_name": bank_name,
            "account_no_masked": masked,
            "added_at": added,
        }

    # ---- pay -------------------------------------------------------------
    def pay_payee(
        self,
        account_id: str,
        payee_id: str,
        amount_minor: int,
        memo: Optional[str] = None,
        scheduled_for: Optional[str] = None,
    ) -> dict:
        if amount_minor is None or int(amount_minor) <= 0:
            raise BadAmountError("amount_minor must be a positive integer")
        amt = int(amount_minor)
        acct = fetch_account(self.conn, account_id)
        payee = self._fetch_payee(payee_id)
        if payee["user_id"] != acct["user_id"]:
            raise PayeeNotFoundError(
                f"payee {payee_id} does not belong to account owner"
            )

        sim_date = today_utc()
        if scheduled_for and parse_date(scheduled_for) > parse_date(sim_date):
            # Future-dated: park as pending, do NOT debit yet.
            seq = next_counter(self.conn, "pending_seq")
            pend = make_pending_id(seq)
            self.conn.execute(
                """
                INSERT INTO pending_payments
                  (pending_id, account_id, payee_id, amount_minor, memo,
                   scheduled_for, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
                """,
                (pend, account_id, payee_id, amt, memo, scheduled_for),
            )
            return {
                "pending_id": pend,
                "tx_id_or_pending_id": pend,
                "status": "scheduled",
                "scheduled_for": scheduled_for,
                "amount_minor": amt,
            }

        # Immediate debit.
        out = post_transaction(
            self.conn,
            account_id=account_id,
            amount_minor=-amt,
            kind="payment",
            sim_date=sim_date,
            counterparty=payee["name"],
            memo=memo,
        )
        return {
            "tx_id": out["tx_id"],
            "tx_id_or_pending_id": out["tx_id"],
            "status": "posted",
            "amount_minor": amt,
            "balance_after_minor": out["balance_after_minor"],
        }

    def _fetch_payee(self, payee_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM payees WHERE payee_id = ?", (payee_id,)
        ).fetchone()
        if not row:
            raise PayeeNotFoundError(f"payee not found: {payee_id}")
        return row
