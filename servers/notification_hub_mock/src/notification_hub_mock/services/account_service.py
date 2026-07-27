"""Official accounts (公众号): subscribe / list / read feed."""
import logging
import sqlite3
from typing import List

from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    AccountNotFoundError,
    AlreadySubscribedError,
    BadArgError,
)
from ._common import official_account_row, post_row

logger = logging.getLogger(__name__)


class OfficialAccountService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def subscribe_official_account(self, user_id: str, account_id: str) -> dict:
        if not user_id or not account_id:
            raise BadArgError("user_id and account_id are required")
        self._fetch_account(account_id)  # raises ACCOUNT_NOT_FOUND
        existing = self.conn.execute(
            "SELECT 1 FROM official_account_subscriptions "
            "WHERE user_id = ? AND account_id = ?",
            (user_id, account_id),
        ).fetchone()
        if existing:
            raise AlreadySubscribedError(
                f"{user_id} already subscribes to {account_id}"
            )
        ts = now_iso_z()
        self.conn.execute(
            "INSERT INTO official_account_subscriptions "
            "(user_id, account_id, subscribed_at) VALUES (?, ?, ?)",
            (user_id, account_id, ts),
        )
        acct = official_account_row(self._fetch_account(account_id))
        acct["subscribed_at"] = ts
        return acct

    def list_official_accounts(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT a.*, s.subscribed_at
            FROM official_account_subscriptions s
            JOIN official_accounts a ON a.account_id = s.account_id
            WHERE s.user_id = ?
            ORDER BY s.subscribed_at ASC, a.account_id ASC
            """,
            (user_id,),
        ).fetchall()
        out = []
        for r in rows:
            d = official_account_row(r)
            d["subscribed_at"] = r["subscribed_at"]
            out.append(d)
        return out

    def get_account_feed(self, account_id: str, limit: int = 20) -> List[dict]:
        self._fetch_account(account_id)  # raises ACCOUNT_NOT_FOUND
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 200:
            limit = 200
        rows = self.conn.execute(
            "SELECT * FROM official_account_posts WHERE account_id = ? "
            "ORDER BY published_at DESC, post_id DESC LIMIT ?",
            (account_id, int(limit)),
        ).fetchall()
        return [post_row(r) for r in rows]

    def _fetch_account(self, account_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM official_accounts WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        if not row:
            raise AccountNotFoundError(f"official account not found: {account_id}")
        return row
