"""User's saved (favourited) listings."""
import logging
import sqlite3
from typing import List

from ..backends.db import next_counter
from ..utils.exceptions import (
    AlreadySavedError,
    BadArgError,
    NotSavedError,
)
from ._repo import fetch_listing, listing_summary, synth_timestamp

logger = logging.getLogger(__name__)


class SavedService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def save_listing(self, user_id: str, listing_id: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        fetch_listing(self.conn, listing_id)  # raises LISTING_NOT_FOUND
        existing = self.conn.execute(
            "SELECT 1 FROM saved_listings WHERE user_id = ? AND listing_id = ?",
            (user_id, listing_id),
        ).fetchone()
        if existing:
            raise AlreadySavedError(
                f"listing {listing_id} already saved by {user_id}"
            )
        seq = next_counter(self.conn, "saved_seq")
        saved_at = synth_timestamp(seq)
        self.conn.execute(
            "INSERT INTO saved_listings (user_id, listing_id, saved_at) VALUES (?, ?, ?)",
            (user_id, listing_id, saved_at),
        )
        return {
            "user_id": user_id,
            "listing_id": listing_id,
            "saved_at": saved_at,
            "status": "saved",
        }

    def unsave_listing(self, user_id: str, listing_id: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        existing = self.conn.execute(
            "SELECT 1 FROM saved_listings WHERE user_id = ? AND listing_id = ?",
            (user_id, listing_id),
        ).fetchone()
        if not existing:
            raise NotSavedError(
                f"listing {listing_id} is not saved by {user_id}"
            )
        self.conn.execute(
            "DELETE FROM saved_listings WHERE user_id = ? AND listing_id = ?",
            (user_id, listing_id),
        )
        return {
            "user_id": user_id,
            "listing_id": listing_id,
            "status": "unsaved",
        }

    def list_saved(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT l.*, s.saved_at AS _saved_at
            FROM saved_listings s
            JOIN listings l ON l.listing_id = s.listing_id
            WHERE s.user_id = ?
            ORDER BY s.saved_at ASC, l.listing_id ASC
            """,
            (user_id,),
        ).fetchall()
        out = []
        for r in rows:
            summary = listing_summary(r)
            summary["saved_at"] = r["_saved_at"]
            out.append(summary)
        return out
