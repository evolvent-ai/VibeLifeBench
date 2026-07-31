"""User read + social graph: profile, user notes, follow/unfollow."""
import logging
import sqlite3
from typing import List

from ..utils.dates import now_iso_z
from ..utils.exceptions import (
    AlreadyExistsError,
    NotFollowingError,
    SelfFollowError,
)
from ._common import fetch_user_row, note_summary

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- profile ---------------------------------------------------------
    def get_user_profile(self, user_id: str) -> dict:
        row = fetch_user_row(self.conn, user_id)
        following = self.conn.execute(
            "SELECT COUNT(*) AS c FROM follows WHERE follower_id = ?", (user_id,)
        ).fetchone()["c"]
        return {
            "user_id": row["user_id"],
            "handle": row["handle"],
            "nickname": row["nickname"],
            "bio": row["bio"],
            "is_official": bool(int(row["is_official"])),
            "follower_count": int(row["follower_count"]),
            "following_count": int(following),
            "note_count": int(row["note_count"]),
            "joined_at": row["joined_at"],
        }

    # ---- user notes ------------------------------------------------------
    def list_user_notes(self, user_id: str) -> List[dict]:
        fetch_user_row(self.conn, user_id)
        rows = self.conn.execute(
            """
            SELECT * FROM notes WHERE author_id = ?
            ORDER BY published_at DESC, note_id DESC
            """,
            (user_id,),
        ).fetchall()
        nickname = self.conn.execute(
            "SELECT nickname FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()["nickname"]
        return [note_summary(r, nickname) for r in rows]

    # ---- follow ----------------------------------------------------------
    def follow_user(self, user_id: str, target_user_id: str) -> dict:
        if user_id == target_user_id:
            raise SelfFollowError("cannot follow yourself")
        fetch_user_row(self.conn, user_id)
        fetch_user_row(self.conn, target_user_id)
        existing = self.conn.execute(
            "SELECT 1 FROM follows WHERE follower_id = ? AND followee_id = ?",
            (user_id, target_user_id),
        ).fetchone()
        if existing:
            raise AlreadyExistsError(
                f"{user_id} already follows {target_user_id}"
            )
        self.conn.execute(
            "INSERT INTO follows (follower_id, followee_id, created_at) VALUES (?, ?, ?)",
            (user_id, target_user_id, now_iso_z()),
        )
        self.conn.execute(
            "UPDATE users SET follower_count = follower_count + 1 WHERE user_id = ?",
            (target_user_id,),
        )
        row = fetch_user_row(self.conn, target_user_id)
        return {
            "follower_id": user_id,
            "followee_id": target_user_id,
            "following": True,
            "followee_follower_count": int(row["follower_count"]),
        }

    def unfollow_user(self, user_id: str, target_user_id: str) -> dict:
        fetch_user_row(self.conn, user_id)
        fetch_user_row(self.conn, target_user_id)
        existing = self.conn.execute(
            "SELECT 1 FROM follows WHERE follower_id = ? AND followee_id = ?",
            (user_id, target_user_id),
        ).fetchone()
        if not existing:
            raise NotFollowingError(
                f"{user_id} does not follow {target_user_id}"
            )
        self.conn.execute(
            "DELETE FROM follows WHERE follower_id = ? AND followee_id = ?",
            (user_id, target_user_id),
        )
        self.conn.execute(
            "UPDATE users SET follower_count = MAX(follower_count - 1, 0) WHERE user_id = ?",
            (target_user_id,),
        )
        row = fetch_user_row(self.conn, target_user_id)
        return {
            "follower_id": user_id,
            "followee_id": target_user_id,
            "following": False,
            "followee_follower_count": int(row["follower_count"]),
        }
