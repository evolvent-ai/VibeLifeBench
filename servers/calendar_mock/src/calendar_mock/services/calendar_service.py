"""Calendar listing service."""
import logging
import sqlite3
from typing import List

from ..utils.exceptions import BadArgError
from ._common import format_calendar

logger = logging.getLogger(__name__)


class CalendarService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_calendars(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT calendar_id, user_id, name, color, timezone, is_primary, created_at
            FROM calendars WHERE user_id = ?
            ORDER BY is_primary DESC, created_at ASC, calendar_id ASC
            """,
            (user_id,),
        ).fetchall()
        return [format_calendar(r) for r in rows]
