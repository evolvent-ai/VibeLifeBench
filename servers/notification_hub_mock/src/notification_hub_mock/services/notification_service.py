"""Notification inbox: list / get / mark read.

Notifications are pre-seeded static rows. This service never creates
notifications — new rows arrive via out-of-band SQL mutation. It only
reads them and flips the ``read`` flag.
"""
import logging
import sqlite3
from typing import List, Optional

from ..utils.dates import parse_date
from ..utils.exceptions import BadArgError, NotificationNotFoundError
from ._common import notification_row

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- list ------------------------------------------------------------
    def list_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        source: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 50,
    ) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 500:
            limit = 500
        if since:
            parse_date(since)  # validates YYYY-MM-DD

        sql = ["SELECT * FROM notifications WHERE user_id = ?"]
        args: List = [user_id]
        if unread_only:
            sql.append("AND read = 0")
        if source:
            sql.append("AND source = ?")
            args.append(source)
        if since:
            sql.append("AND substr(created_at, 1, 10) >= ?")
            args.append(since)
        sql.append("ORDER BY created_at DESC, notification_id DESC LIMIT ?")
        args.append(int(limit))
        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [notification_row(r) for r in rows]

    def get_notification(self, notification_id: str) -> dict:
        return notification_row(self._fetch(notification_id))

    # ---- mark read -------------------------------------------------------
    def mark_read(self, notification_id: str) -> dict:
        self._fetch(notification_id)
        self.conn.execute(
            "UPDATE notifications SET read = 1 WHERE notification_id = ?",
            (notification_id,),
        )
        return notification_row(self._fetch(notification_id))

    def mark_all_read(self, user_id: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        before = self.conn.execute(
            "SELECT COUNT(*) AS c FROM notifications WHERE user_id = ? AND read = 0",
            (user_id,),
        ).fetchone()
        self.conn.execute(
            "UPDATE notifications SET read = 1 WHERE user_id = ? AND read = 0",
            (user_id,),
        )
        return {"user_id": user_id, "marked_read": int(before["c"])}

    # ---- internals -------------------------------------------------------
    def _fetch(self, notification_id: str) -> sqlite3.Row:
        row = self.conn.execute(
            "SELECT * FROM notifications WHERE notification_id = ?",
            (notification_id,),
        ).fetchone()
        if not row:
            raise NotificationNotFoundError(
                f"notification not found: {notification_id}"
            )
        return row
