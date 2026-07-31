"""Zero-padded counter-based id generators backed by the ``_counters`` table."""

import sqlite3
from typing import Final

_PREFIXES: Final = {
    "application": "va",
    "document": "doc",
    "subscription": "sub",
    "notification": "notif",
}

_PADDING = 4


class IdGenerator:
    """Issues monotonically-increasing zero-padded ids backed by ``_counters``.

    Each entity kind uses its own row in ``_counters`` keyed by name.
    """

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _next(self, kind: str) -> int:
        self.conn.execute(
            "INSERT INTO _counters(name, value) VALUES(?, 0) "
            "ON CONFLICT(name) DO NOTHING",
            (kind,),
        )
        self.conn.execute(
            "UPDATE _counters SET value = value + 1 WHERE name = ?", (kind,)
        )
        row = self.conn.execute(
            "SELECT value FROM _counters WHERE name = ?", (kind,)
        ).fetchone()
        return int(row[0])

    def application_id(self) -> str:
        return f"{_PREFIXES['application']}_{self._next('application'):0{_PADDING}d}"

    def document_id(self) -> str:
        return f"{_PREFIXES['document']}_{self._next('document'):0{_PADDING}d}"

    def subscription_id(self) -> str:
        return f"{_PREFIXES['subscription']}_{self._next('subscription'):0{_PADDING}d}"

    def notification_id(self) -> str:
        return f"{_PREFIXES['notification']}_{self._next('notification'):0{_PADDING}d}"
