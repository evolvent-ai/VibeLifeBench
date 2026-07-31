"""Read-only tracking lookups.

Wraps the ``track_package`` agent tool plus the list-by-user view. All
heavy mutating code lives elsewhere; this file is intentionally lean.
"""
import json
import logging
import sqlite3
from typing import Optional

from ..utils.exceptions import BadArgError
from ._common import address_summary, fetch_shipment_row

logger = logging.getLogger(__name__)


def _events_for(conn: sqlite3.Connection, shipment_id: str) -> list[dict]:
    rows = conn.execute(
        "SELECT at, location, status_code, description FROM shipment_events "
        "WHERE shipment_id = ? ORDER BY at ASC, event_id ASC",
        (shipment_id,),
    ).fetchall()
    return [
        {
            "at": r["at"],
            "location": r["location"],
            "status_code": r["status_code"],
            "description": r["description"],
        }
        for r in rows
    ]


class TrackingService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def track_package(self, tracking_no: str) -> dict:
        if not tracking_no or not isinstance(tracking_no, str):
            raise BadArgError("tracking_no must be a non-empty string")
        row = fetch_shipment_row(self.conn, tracking_no=tracking_no)
        events = _events_for(self.conn, row["shipment_id"])
        latest = events[-1] if events else None
        sender = json.loads(row["sender_json"])
        recipient = json.loads(row["recipient_json"])
        return {
            "tracking_no": row["tracking_no"],
            "carrier": row["carrier"],
            "status": row["status"],
            "latest_event": latest,
            "origin": address_summary(sender),
            "destination": address_summary(recipient),
            "eta_date": row["eta_date"],
            "events": events,
        }

    def list_shipments(
        self,
        user_id: str,
        status_filter: Optional[str] = None,
        limit: int = 20,
    ) -> dict:
        if not user_id or not isinstance(user_id, str):
            raise BadArgError("user_id must be a non-empty string")
        try:
            limit_int = int(limit)
        except Exception:
            raise BadArgError("limit must be an integer")
        if limit_int <= 0:
            raise BadArgError("limit must be positive")

        params: list = [user_id]
        sql = "SELECT * FROM shipments WHERE user_id = ?"
        if status_filter:
            sql += " AND status = ?"
            params.append(status_filter)
        sql += " ORDER BY created_at DESC, shipment_id DESC LIMIT ?"
        params.append(limit_int)
        rows = self.conn.execute(sql, params).fetchall()

        items = []
        for row in rows:
            sender = json.loads(row["sender_json"])
            recipient = json.loads(row["recipient_json"])
            items.append(
                {
                    "shipment_id": row["shipment_id"],
                    "tracking_no": row["tracking_no"],
                    "carrier": row["carrier"],
                    "service_level": row["service_level"],
                    "status": row["status"],
                    "origin": address_summary(sender),
                    "destination": address_summary(recipient),
                    "weight_kg": float(row["weight_kg"]),
                    "fee_minor": int(row["fee_minor"]),
                    "created_at": row["created_at"],
                    "eta_date": row["eta_date"],
                }
            )
        return {
            "user_id": user_id,
            "count": len(items),
            "items": items,
        }
