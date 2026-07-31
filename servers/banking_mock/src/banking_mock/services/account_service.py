"""Read-side account queries: list/get + transaction history."""
import logging
import sqlite3
from typing import List, Optional

from ..utils.dates import add_days, parse_date, today_utc
from ..utils.exceptions import BadArgError
from ._posting import fetch_account

logger = logging.getLogger(__name__)

VALID_KINDS = (
    "deposit", "withdrawal", "transfer_in", "transfer_out",
    "payment", "fee", "interest",
)


class AccountService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- list ------------------------------------------------------------
    def list_accounts(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT account_id, type, name, balance_minor, currency, opened_at, frozen
            FROM accounts WHERE user_id = ? ORDER BY opened_at ASC, account_id ASC
            """,
            (user_id,),
        ).fetchall()
        return [
            {
                "account_id": r["account_id"],
                "type": r["type"],
                "name": r["name"],
                "balance_minor": int(r["balance_minor"]),
                "currency": r["currency"],
                "opened_at": r["opened_at"],
                "frozen": bool(int(r["frozen"])),
            }
            for r in rows
        ]

    # ---- detail ----------------------------------------------------------
    def get_account(self, account_id: str) -> dict:
        row = fetch_account(self.conn, account_id)
        trend = self._balance_trend(account_id, days=7)
        return {
            "account_id": row["account_id"],
            "user_id": row["user_id"],
            "type": row["type"],
            "name": row["name"],
            "balance_minor": int(row["balance_minor"]),
            "currency": row["currency"],
            "opened_at": row["opened_at"],
            "frozen": bool(int(row["frozen"])),
            "balance_trend_7d": trend,
        }

    def _balance_trend(self, account_id: str, days: int) -> List[dict]:
        """Derived view: one balance snapshot per day for the last ``days`` days.

        Each snapshot is the balance_after_minor of the latest tx on or
        before that day, falling back to 0 if no tx exists yet.
        """
        end_date = today_utc()
        start_date = add_days(end_date, -(days - 1))

        snapshots: List[dict] = []
        cur = start_date
        while parse_date(cur) <= parse_date(end_date):
            row = self.conn.execute(
                """
                SELECT balance_after_minor FROM transactions
                WHERE account_id = ? AND substr(posted_at, 1, 10) <= ?
                ORDER BY posted_at DESC, tx_id DESC LIMIT 1
                """,
                (account_id, cur),
            ).fetchone()
            snapshots.append({
                "date": cur,
                "balance_minor": int(row["balance_after_minor"]) if row else 0,
            })
            cur = add_days(cur, 1)
        return snapshots

    # ---- transactions ----------------------------------------------------
    def list_transactions(
        self,
        account_id: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 50,
        kind_filter: Optional[str] = None,
    ) -> List[dict]:
        fetch_account(self.conn, account_id)  # raises ACCOUNT_NOT_FOUND
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 500:
            limit = 500
        if kind_filter is not None and kind_filter not in VALID_KINDS:
            raise BadArgError(f"kind_filter must be one of {VALID_KINDS}")
        if since:
            parse_date(since)
        if until:
            parse_date(until)

        sql = [
            "SELECT tx_id, account_id, posted_at, amount_minor, kind, "
            "counterparty, memo, balance_after_minor FROM transactions "
            "WHERE account_id = ?"
        ]
        args: List = [account_id]
        if since:
            sql.append("AND substr(posted_at, 1, 10) >= ?")
            args.append(since)
        if until:
            sql.append("AND substr(posted_at, 1, 10) <= ?")
            args.append(until)
        if kind_filter:
            sql.append("AND kind = ?")
            args.append(kind_filter)
        sql.append("ORDER BY posted_at DESC, tx_id DESC LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [
            {
                "tx_id": r["tx_id"],
                "posted_at": r["posted_at"],
                "amount_minor": int(r["amount_minor"]),
                "kind": r["kind"],
                "counterparty": r["counterparty"],
                "memo": r["memo"],
                "balance_after_minor": int(r["balance_after_minor"]),
            }
            for r in rows
        ]
