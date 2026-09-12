"""Engagement: like, collect/uncollect, list_collections."""
import logging
import sqlite3
from typing import List

from ..utils.dates import now_iso_z
from ..utils.exceptions import AlreadyExistsError, NotCollectedError
from ._common import fetch_note_row, fetch_user_row, note_summary

logger = logging.getLogger(__name__)


class EngagementService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def _nickname(self, author_id: str) -> str:
        row = self.conn.execute(
            "SELECT nickname FROM users WHERE user_id = ?", (author_id,)
        ).fetchone()
        return row["nickname"] if row else author_id

    # ---- like ------------------------------------------------------------
    def like_note(self, user_id: str, note_id: str) -> dict:
        fetch_user_row(self.conn, user_id)
        fetch_note_row(self.conn, note_id)
        existing = self.conn.execute(
            "SELECT 1 FROM likes WHERE user_id = ? AND note_id = ?",
            (user_id, note_id),
        ).fetchone()
        if existing:
            raise AlreadyExistsError(f"{user_id} already liked {note_id}")
        self.conn.execute(
            "INSERT INTO likes (user_id, note_id, created_at) VALUES (?, ?, ?)",
            (user_id, note_id, now_iso_z()),
        )
        self.conn.execute(
            "UPDATE notes SET like_count = like_count + 1 WHERE note_id = ?",
            (note_id,),
        )
        row = fetch_note_row(self.conn, note_id)
        return {
            "user_id": user_id,
            "note_id": note_id,
            "liked": True,
            "like_count": int(row["like_count"]),
        }

    # ---- collect ---------------------------------------------------------
    def collect_note(self, user_id: str, note_id: str) -> dict:
        fetch_user_row(self.conn, user_id)
        fetch_note_row(self.conn, note_id)
        existing = self.conn.execute(
            "SELECT 1 FROM collections WHERE user_id = ? AND note_id = ?",
            (user_id, note_id),
        ).fetchone()
        if existing:
            raise AlreadyExistsError(f"{user_id} already collected {note_id}")
        self.conn.execute(
            "INSERT INTO collections (user_id, note_id, created_at) VALUES (?, ?, ?)",
            (user_id, note_id, now_iso_z()),
        )
        self.conn.execute(
            "UPDATE notes SET collect_count = collect_count + 1 WHERE note_id = ?",
            (note_id,),
        )
        row = fetch_note_row(self.conn, note_id)
        return {
            "user_id": user_id,
            "note_id": note_id,
            "collected": True,
            "collect_count": int(row["collect_count"]),
        }

    def uncollect_note(self, user_id: str, note_id: str) -> dict:
        fetch_user_row(self.conn, user_id)
        fetch_note_row(self.conn, note_id)
        existing = self.conn.execute(
            "SELECT 1 FROM collections WHERE user_id = ? AND note_id = ?",
            (user_id, note_id),
        ).fetchone()
        if not existing:
            raise NotCollectedError(f"{user_id} has not collected {note_id}")
        self.conn.execute(
            "DELETE FROM collections WHERE user_id = ? AND note_id = ?",
            (user_id, note_id),
        )
        self.conn.execute(
            "UPDATE notes SET collect_count = MAX(collect_count - 1, 0) WHERE note_id = ?",
            (note_id,),
        )
        row = fetch_note_row(self.conn, note_id)
        return {
            "user_id": user_id,
            "note_id": note_id,
            "collected": False,
            "collect_count": int(row["collect_count"]),
        }

    def list_collections(self, user_id: str) -> List[dict]:
        fetch_user_row(self.conn, user_id)
        rows = self.conn.execute(
            """
            SELECT n.*, c.created_at AS collected_at
            FROM collections c JOIN notes n ON n.note_id = c.note_id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC, n.note_id DESC
            """,
            (user_id,),
        ).fetchall()
        out = []
        for r in rows:
            item = note_summary(r, self._nickname(r["author_id"]))
            item["collected_at"] = r["collected_at"]
            out.append(item)
        return out
