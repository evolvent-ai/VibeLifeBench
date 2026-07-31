"""Row-fetch + serialization helpers shared across services.

Services operate on an existing ``sqlite3.Connection``. They never import
FastMCP. JSON columns (``tags``, ``image_captions``) are decoded here.
"""
import json
import sqlite3
from typing import List

from ..utils.exceptions import NoteNotFoundError, TopicNotFoundError, UserNotFoundError


def decode_json_list(raw) -> List[str]:
    """Decode a TEXT JSON-array column into a Python list of strings."""
    if not raw:
        return []
    try:
        value = json.loads(raw)
    except (ValueError, TypeError):
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return []


def fetch_note_row(conn: sqlite3.Connection, note_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM notes WHERE note_id = ?", (note_id,)
    ).fetchone()
    if not row:
        raise NoteNotFoundError(f"note not found: {note_id}")
    return row


def fetch_user_row(conn: sqlite3.Connection, user_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    if not row:
        raise UserNotFoundError(f"user not found: {user_id}")
    return row


def fetch_topic_row_by_name(conn: sqlite3.Connection, name: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM topics WHERE name = ?", (name,)
    ).fetchone()
    if not row:
        raise TopicNotFoundError(f"topic not found: {name}")
    return row


def note_summary(row: sqlite3.Row, author_nickname: str) -> dict:
    """Compact note shape used in list/search/feed responses."""
    return {
        "note_id": row["note_id"],
        "title": row["title"],
        "category": row["category"],
        "author_id": row["author_id"],
        "author_nickname": author_nickname,
        "tags": decode_json_list(row["tags"]),
        "like_count": int(row["like_count"]),
        "collect_count": int(row["collect_count"]),
        "comment_count": int(row["comment_count"]),
        "published_at": row["published_at"],
    }


def note_detail(row: sqlite3.Row, author: dict) -> dict:
    """Full note shape used by get_note."""
    return {
        "note_id": row["note_id"],
        "title": row["title"],
        "body": row["body"],
        "category": row["category"],
        "tags": decode_json_list(row["tags"]),
        "image_captions": decode_json_list(row["image_captions"]),
        "author": author,
        "like_count": int(row["like_count"]),
        "collect_count": int(row["collect_count"]),
        "comment_count": int(row["comment_count"]),
        "view_count": int(row["view_count"]),
        "published_at": row["published_at"],
    }


def user_brief(row: sqlite3.Row) -> dict:
    return {
        "user_id": row["user_id"],
        "handle": row["handle"],
        "nickname": row["nickname"],
        "is_official": bool(int(row["is_official"])),
    }
