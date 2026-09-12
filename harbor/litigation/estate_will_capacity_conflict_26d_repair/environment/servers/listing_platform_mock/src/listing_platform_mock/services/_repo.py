"""Shared row-fetch + serialization helpers for listing_platform services.

No wall clock / RNG: any timestamp written by a tool is a deterministic
ISO-8601 string derived from a ``_counters`` sequence so re-runs are stable.
"""
import json
import sqlite3
from typing import Optional

from ..utils.exceptions import (
    AgentNotFoundError,
    ListingNotFoundError,
)

# Deterministic synthetic "now": tool-created rows get a stable, monotonically
# increasing timestamp seeded off a counter. The server has no real clock; the
# task-level reference date for the shipped scenario env is 2026-05-20.
_SYNTH_BASE = "2026-05-20T00:00:00+08:00"
_SYNTH_BASE_DATE = "2026-05-20"


def synth_timestamp(seq: int) -> str:
    """A deterministic ISO-8601 timestamp (Asia/Shanghai) for tool-created rows.

    ``seq`` (a counter value) maps to a fixed minute offset, so identical
    operation sequences always produce identical timestamps.
    """
    minute = seq % 60
    hour = (seq // 60) % 24
    return f"{_SYNTH_BASE_DATE}T{hour:02d}:{minute:02d}:00+08:00"


def fetch_listing(conn: sqlite3.Connection, listing_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM listings WHERE listing_id = ?", (listing_id,)
    ).fetchone()
    if not row:
        raise ListingNotFoundError(f"listing not found: {listing_id}")
    return row


def fetch_agent(conn: sqlite3.Connection, agent_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM agents WHERE agent_id = ?", (agent_id,)
    ).fetchone()
    if not row:
        raise AgentNotFoundError(f"agent not found: {agent_id}")
    return row


def _loads(text: Optional[str], default):
    if text is None or text == "":
        return default
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return default


def listing_summary(row: sqlite3.Row) -> dict:
    """Compact listing view used by search results and list endpoints."""
    return {
        "listing_id": row["listing_id"],
        "category": row["category"],
        "title": row["title"],
        "city": row["city"],
        "district": row["district"],
        "community": row["community"],
        "price_minor": int(row["price_minor"]),
        "area_sqm": row["area_sqm"],
        "rooms": row["rooms"],
        "metro": row["metro"],
        "agent_id": row["agent_id"],
        "status": row["status"],
        "listed_at": row["listed_at"],
    }


def listing_detail(row: sqlite3.Row) -> dict:
    """Full listing view including flexible attrs + photo captions."""
    out = listing_summary(row)
    out["attrs"] = _loads(row["attrs_json"], {})
    out["photos"] = _loads(row["photos_json"], [])
    out["description"] = row["description"]
    out["owner_user_id"] = row["owner_user_id"]
    return out


def agent_view(row: sqlite3.Row) -> dict:
    return {
        "agent_id": row["agent_id"],
        "name": row["name"],
        "agency": row["agency"],
        "phone": row["phone"],
        "rating": row["rating"],
        "deals_count": int(row["deals_count"]),
        "service_area": row["service_area"],
    }
