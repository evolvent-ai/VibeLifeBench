"""User lookup.

Only ``get_self`` is fully implemented per the priority list — the other
two user endpoints (``get-user`` and ``get-users``) are stubbed at the
tool layer.
"""
import logging
import sqlite3
from typing import Any, Dict

from ..models import row_to_user
from ..utils.exceptions import UserNotFoundError

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_self(self) -> Dict[str, Any]:
        """Return the seeded "bot" user, or the first person user as a fallback.

        Matches the legacy pg-client semantics: prefer a row with
        type='bot'; otherwise return the first user; otherwise raise.
        """
        row = self.conn.execute(
            "SELECT * FROM users WHERE type = 'bot' ORDER BY user_id LIMIT 1"
        ).fetchone()
        if row is None:
            row = self.conn.execute(
                "SELECT * FROM users ORDER BY user_id LIMIT 1"
            ).fetchone()
        if row is None:
            raise UserNotFoundError("no user seeded")
        out = row_to_user(row)
        # Real Notion ``get-self`` includes the bot owner block.
        out.setdefault("bot", {"owner": {"type": "user"}})
        return out
