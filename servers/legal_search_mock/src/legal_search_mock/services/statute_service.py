"""Read-side statute queries: search, metadata, articles, article full text."""
import logging
import sqlite3
from typing import List, Optional

from ..utils.exceptions import BadArgError
from ._common import fetch_article, fetch_statute

logger = logging.getLogger(__name__)


class StatuteService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- search ----------------------------------------------------------
    def search_statutes(
        self, keyword: Optional[str] = None, limit: int = 20
    ) -> List[dict]:
        if limit is None or limit < 1:
            raise BadArgError("limit must be >= 1")
        if limit > 100:
            limit = 100

        sql = ["SELECT * FROM statutes WHERE 1=1"]
        args: List = []
        if keyword:
            like = f"%{keyword}%"
            sql.append(
                "AND (name LIKE ? OR short_name LIKE ? OR summary LIKE ?)"
            )
            args.extend([like, like, like])
        sql.append("ORDER BY effective_date DESC, statute_id ASC LIMIT ?")
        args.append(int(limit))

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [self._statute_dict(r) for r in rows]

    # ---- metadata --------------------------------------------------------
    def get_statute(self, statute_id: str) -> dict:
        row = fetch_statute(self.conn, statute_id)
        n = self.conn.execute(
            "SELECT COUNT(*) AS c FROM statute_articles WHERE statute_id = ?",
            (statute_id,),
        ).fetchone()["c"]
        d = self._statute_dict(row)
        d["article_count"] = int(n)
        return d

    # ---- articles --------------------------------------------------------
    def list_statute_articles(self, statute_id: str) -> List[dict]:
        fetch_statute(self.conn, statute_id)  # raises STATUTE_NOT_FOUND
        rows = self.conn.execute(
            """
            SELECT * FROM statute_articles WHERE statute_id = ?
            ORDER BY seq ASC, article_id ASC
            """,
            (statute_id,),
        ).fetchall()
        return [
            {
                "article_id": r["article_id"],
                "statute_id": r["statute_id"],
                "article_no": r["article_no"],
                "heading": r["heading"],
            }
            for r in rows
        ]

    def get_article(self, article_id: str) -> dict:
        row = fetch_article(self.conn, article_id)
        stat = fetch_statute(self.conn, row["statute_id"])
        return {
            "article_id": row["article_id"],
            "statute_id": row["statute_id"],
            "statute_name": stat["name"],
            "article_no": row["article_no"],
            "heading": row["heading"],
            "text": row["text"],
        }

    # ---- helpers ---------------------------------------------------------
    def _statute_dict(self, r: sqlite3.Row) -> dict:
        return {
            "statute_id": r["statute_id"],
            "name": r["name"],
            "short_name": r["short_name"],
            "issuer": r["issuer"],
            "effective_date": r["effective_date"],
            "status": r["status"],
            "summary": r["summary"],
        }
