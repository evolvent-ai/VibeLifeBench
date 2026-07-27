"""Scheduling + management of property viewings (看房预约)."""
import logging
import sqlite3
from typing import List

from ..backends.db import next_counter
from ..utils.dates import parse_datetime
from ..utils.exceptions import (
    BadArgError,
    ListingDelistedError,
    ViewingNotFoundError,
)
from ..utils.ids import viewing_id as make_viewing_id
from ._repo import fetch_listing, synth_timestamp

logger = logging.getLogger(__name__)


class ViewingService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def schedule_viewing(self, user_id: str, listing_id: str, datetime_str: str) -> dict:
        if not user_id:
            raise BadArgError("user_id is required")
        parse_datetime(datetime_str)  # validates ISO-8601, raises BAD_DATE
        row = fetch_listing(self.conn, listing_id)
        if row["status"] != "active":
            raise ListingDelistedError(f"listing {listing_id} is delisted")
        agent_id = row["agent_id"]
        seq = next_counter(self.conn, "viewing_seq")
        vid = make_viewing_id(seq)
        created = synth_timestamp(seq)
        self.conn.execute(
            """
            INSERT INTO viewings (viewing_id, user_id, listing_id, agent_id, scheduled_at, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'scheduled', ?)
            """,
            (vid, user_id, listing_id, agent_id, datetime_str, created),
        )
        return {
            "viewing_id": vid,
            "user_id": user_id,
            "listing_id": listing_id,
            "agent_id": agent_id,
            "scheduled_at": datetime_str,
            "status": "scheduled",
            "created_at": created,
        }

    def list_viewings(self, user_id: str) -> List[dict]:
        if not user_id:
            raise BadArgError("user_id is required")
        rows = self.conn.execute(
            """
            SELECT v.viewing_id, v.listing_id, v.agent_id, v.scheduled_at, v.status, v.created_at,
                   l.title AS listing_title, l.community AS listing_community
            FROM viewings v
            LEFT JOIN listings l ON l.listing_id = v.listing_id
            WHERE v.user_id = ?
            ORDER BY v.scheduled_at ASC, v.viewing_id ASC
            """,
            (user_id,),
        ).fetchall()
        return [
            {
                "viewing_id": r["viewing_id"],
                "listing_id": r["listing_id"],
                "listing_title": r["listing_title"],
                "listing_community": r["listing_community"],
                "agent_id": r["agent_id"],
                "scheduled_at": r["scheduled_at"],
                "status": r["status"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    def cancel_viewing(self, viewing_id: str) -> dict:
        row = self.conn.execute(
            "SELECT * FROM viewings WHERE viewing_id = ?", (viewing_id,)
        ).fetchone()
        if not row:
            raise ViewingNotFoundError(f"viewing not found: {viewing_id}")
        self.conn.execute(
            "UPDATE viewings SET status = 'cancelled' WHERE viewing_id = ?",
            (viewing_id,),
        )
        return {
            "viewing_id": viewing_id,
            "status": "cancelled",
        }
