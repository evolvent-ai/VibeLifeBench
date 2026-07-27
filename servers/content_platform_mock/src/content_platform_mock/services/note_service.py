"""Note discovery + read + authoring: search, get, comments, trending, publish."""
import json
import logging
import sqlite3
from typing import List, Optional

from ..backends.db import next_counter
from ..utils.dates import now_iso_z, today_utc
from ..utils.exceptions import BadArgError
from ..utils.ids import comment_id as make_comment_id
from ..utils.ids import note_id as make_note_id
from ._common import (
    fetch_note_row,
    fetch_user_row,
    note_detail,
    note_summary,
)

logger = logging.getLogger(__name__)

VALID_CATEGORIES = ("备考", "装修", "健身", "旅行", "母婴", "其他")
VALID_SORTS = ("hot", "latest", "most_collected")
DEFAULT_LIMIT = 20
MAX_LIMIT = 100


class NoteService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- helpers ---------------------------------------------------------
    def _nickname(self, author_id: str) -> str:
        row = self.conn.execute(
            "SELECT nickname FROM users WHERE user_id = ?", (author_id,)
        ).fetchone()
        return row["nickname"] if row else author_id

    def _clamp_limit(self, limit: Optional[int]) -> int:
        if limit is None:
            return DEFAULT_LIMIT
        if limit < 1:
            raise BadArgError("limit must be >= 1")
        return min(int(limit), MAX_LIMIT)

    def _order_clause(self, sort: str) -> str:
        if sort == "latest":
            return "ORDER BY published_at DESC, note_id DESC"
        if sort == "most_collected":
            return "ORDER BY collect_count DESC, note_id ASC"
        # hot: weighted engagement
        return "ORDER BY (like_count + collect_count * 2 + comment_count * 3) DESC, note_id ASC"

    # ---- search ----------------------------------------------------------
    def search_notes(
        self,
        keyword: str,
        category: Optional[str] = None,
        sort: str = "hot",
        limit: Optional[int] = None,
    ) -> List[dict]:
        if not keyword or not keyword.strip():
            raise BadArgError("keyword is required")
        if category is not None and category not in VALID_CATEGORIES:
            raise BadArgError(f"category must be one of {VALID_CATEGORIES}")
        if sort not in VALID_SORTS:
            raise BadArgError(f"sort must be one of {VALID_SORTS}")
        lim = self._clamp_limit(limit)

        like = f"%{keyword.strip()}%"
        sql = [
            "SELECT * FROM notes WHERE (title LIKE ? OR body LIKE ? OR tags LIKE ?)"
        ]
        args: List = [like, like, like]
        if category:
            sql.append("AND category = ?")
            args.append(category)
        sql.append(self._order_clause(sort))
        sql.append("LIMIT ?")
        args.append(lim)

        rows = self.conn.execute(" ".join(sql), args).fetchall()
        return [note_summary(r, self._nickname(r["author_id"])) for r in rows]

    # ---- get -------------------------------------------------------------
    def get_note(self, note_id: str) -> dict:
        row = fetch_note_row(self.conn, note_id)
        author = fetch_user_row(self.conn, row["author_id"])
        author_brief = {
            "user_id": author["user_id"],
            "handle": author["handle"],
            "nickname": author["nickname"],
            "is_official": bool(int(author["is_official"])),
            "follower_count": int(author["follower_count"]),
        }
        return note_detail(row, author_brief)

    # ---- comments --------------------------------------------------------
    def get_note_comments(self, note_id: str, limit: Optional[int] = None) -> List[dict]:
        fetch_note_row(self.conn, note_id)  # raises NOTE_NOT_FOUND
        lim = self._clamp_limit(limit)
        rows = self.conn.execute(
            """
            SELECT c.comment_id, c.note_id, c.user_id, c.body, c.like_count,
                   c.created_at, u.nickname AS nickname
            FROM comments c LEFT JOIN users u ON u.user_id = c.user_id
            WHERE c.note_id = ?
            ORDER BY c.created_at ASC, c.comment_id ASC LIMIT ?
            """,
            (note_id, lim),
        ).fetchall()
        return [
            {
                "comment_id": r["comment_id"],
                "note_id": r["note_id"],
                "user_id": r["user_id"],
                "nickname": r["nickname"] or r["user_id"],
                "body": r["body"],
                "like_count": int(r["like_count"]),
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    def post_comment(self, note_id: str, user_id: str, body: str) -> dict:
        fetch_note_row(self.conn, note_id)
        fetch_user_row(self.conn, user_id)
        if not body or not body.strip():
            raise BadArgError("body is required")

        seq = next_counter(self.conn, "comment_seq")
        cid = make_comment_id(seq)
        created_at = now_iso_z()
        self.conn.execute(
            """
            INSERT INTO comments (comment_id, note_id, user_id, body, like_count, created_at)
            VALUES (?, ?, ?, ?, 0, ?)
            """,
            (cid, note_id, user_id, body.strip(), created_at),
        )
        self.conn.execute(
            "UPDATE notes SET comment_count = comment_count + 1 WHERE note_id = ?",
            (note_id,),
        )
        return {
            "comment_id": cid,
            "note_id": note_id,
            "user_id": user_id,
            "body": body.strip(),
            "created_at": created_at,
        }

    # ---- trending --------------------------------------------------------
    def get_trending(self, category: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
        if category is not None and category not in VALID_CATEGORIES:
            raise BadArgError(f"category must be one of {VALID_CATEGORIES}")
        lim = self._clamp_limit(limit)
        sql = ["SELECT * FROM notes"]
        args: List = []
        if category:
            sql.append("WHERE category = ?")
            args.append(category)
        sql.append(self._order_clause("hot"))
        sql.append("LIMIT ?")
        args.append(lim)
        rows = self.conn.execute(" ".join(sql), args).fetchall()
        out = []
        for rank, r in enumerate(rows, start=1):
            item = note_summary(r, self._nickname(r["author_id"]))
            item["rank"] = rank
            item["view_count"] = int(r["view_count"])
            out.append(item)
        return out

    # ---- publish ---------------------------------------------------------
    def publish_note(
        self,
        user_id: str,
        title: str,
        body: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        image_captions: Optional[List[str]] = None,
    ) -> dict:
        fetch_user_row(self.conn, user_id)
        if not title or not title.strip():
            raise BadArgError("title is required")
        if not body or not body.strip():
            raise BadArgError("body is required")
        cat = category or "其他"
        if cat not in VALID_CATEGORIES:
            raise BadArgError(f"category must be one of {VALID_CATEGORIES}")
        tag_list = [str(t) for t in (tags or [])]
        cap_list = [str(c) for c in (image_captions or [])]

        seq = next_counter(self.conn, "note_seq")
        nid = make_note_id(seq)
        published_at = today_utc()
        self.conn.execute(
            """
            INSERT INTO notes (
                note_id, author_id, title, body, category, tags, image_captions,
                like_count, collect_count, comment_count, view_count, published_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 0, ?)
            """,
            (
                nid,
                user_id,
                title.strip(),
                body.strip(),
                cat,
                json.dumps(tag_list, ensure_ascii=False),
                json.dumps(cap_list, ensure_ascii=False),
                published_at,
            ),
        )
        self.conn.execute(
            "UPDATE users SET note_count = note_count + 1 WHERE user_id = ?",
            (user_id,),
        )
        return {
            "note_id": nid,
            "author_id": user_id,
            "title": title.strip(),
            "category": cat,
            "tags": tag_list,
            "image_captions": cap_list,
            "published_at": published_at,
        }
