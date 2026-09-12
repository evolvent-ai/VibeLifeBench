"""Read-side court directory queries."""
import logging
import sqlite3
from typing import List

from ._common import fetch_court

logger = logging.getLogger(__name__)


class CourtService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def list_courts(self) -> List[dict]:
        rows = self.conn.execute(
            "SELECT * FROM courts ORDER BY court_id ASC"
        ).fetchall()
        return [self._court_dict(r) for r in rows]

    def get_court(self, court_id: str) -> dict:
        row = fetch_court(self.conn, court_id)
        n = self.conn.execute(
            "SELECT COUNT(*) AS c FROM cases WHERE court_id = ?", (court_id,)
        ).fetchone()["c"]
        d = self._court_dict(row)
        d["case_count"] = int(n)
        return d

    def _court_dict(self, r: sqlite3.Row) -> dict:
        return {
            "court_id": r["court_id"],
            "name": r["name"],
            "level": r["level"],
            "region": r["region"],
        }
