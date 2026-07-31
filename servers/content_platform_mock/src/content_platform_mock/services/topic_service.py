"""Topics (话题): search_topics + get_topic_feed."""
import logging
import sqlite3
from typing import List, Optional

from ..utils.exceptions import BadArgError
from ._common import fetch_topic_row_by_name, note_summary

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


class TopicService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def _nickname(self, author_id: str) -> str:
        row = self.conn.execute(
            "SELECT nickname FROM users WHERE user_id = ?", (author_id,)
        ).fetchone()
        return row["nickname"] if row else author_id

    def search_topics(self, keyword: str) -> List[dict]:
        if not keyword or not keyword.strip():
            raise BadArgError("keyword is required")
        like = f"%{keyword.strip()}%"
        rows = self.conn.execute(
            """
            SELECT * FROM topics
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY view_count DESC, topic_id ASC
            """,
            (like, like),
        ).fetchall()
        return [
            {
                "topic_id": r["topic_id"],
                "name": r["name"],
                "category": r["category"],
                "description": r["description"],
                "note_count": int(r["note_count"]),
                "view_count": int(r["view_count"]),
            }
            for r in rows
        ]

    def get_topic_feed(self, topic: str, limit: Optional[int] = None) -> dict:
        topic_row = fetch_topic_row_by_name(self.conn, topic)
        if limit is None:
            lim = DEFAULT_LIMIT
        elif limit < 1:
            raise BadArgError("limit must be >= 1")
        else:
            lim = min(int(limit), MAX_LIMIT)

        rows = self.conn.execute(
            """
            SELECT n.* FROM note_topics nt JOIN notes n ON n.note_id = nt.note_id
            WHERE nt.topic_id = ?
            ORDER BY (n.like_count + n.collect_count * 2 + n.comment_count * 3) DESC, n.note_id ASC
            LIMIT ?
            """,
            (topic_row["topic_id"], lim),
        ).fetchall()
        return {
            "topic_id": topic_row["topic_id"],
            "name": topic_row["name"],
            "category": topic_row["category"],
            "description": topic_row["description"],
            "note_count": int(topic_row["note_count"]),
            "view_count": int(topic_row["view_count"]),
            "notes": [note_summary(r, self._nickname(r["author_id"])) for r in rows],
        }
