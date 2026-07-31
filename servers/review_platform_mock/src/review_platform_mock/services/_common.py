"""Low-level row fetchers + serializers shared across services.

These functions operate on an existing ``sqlite3.Connection``.
"""
import sqlite3

from ..utils.exceptions import (
    DealNotFoundError,
    MerchantNotFoundError,
)
from ..utils.ids import rating_to_float


def fetch_merchant(conn: sqlite3.Connection, merchant_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM merchants WHERE merchant_id = ?", (merchant_id,)
    ).fetchone()
    if not row:
        raise MerchantNotFoundError(f"merchant not found: {merchant_id}")
    return row


def fetch_deal(conn: sqlite3.Connection, deal_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM deals WHERE deal_id = ?", (deal_id,)
    ).fetchone()
    if not row:
        raise DealNotFoundError(f"deal not found: {deal_id}")
    return row


def merchant_summary(row: sqlite3.Row) -> dict:
    """Compact merchant shape used by list/search/recommendation results."""
    return {
        "merchant_id": row["merchant_id"],
        "name": row["name"],
        "category": row["category"],
        "city": row["city"],
        "area": row["area"],
        "rating": rating_to_float(row["rating_tenths"]),
        "review_count": int(row["review_count"]),
        "avg_price_minor": int(row["avg_price_minor"]),
        "price_band": row["price_band"],
        "has_private_room": bool(int(row["has_private_room"])),
        "max_party_size": int(row["max_party_size"]),
        "tags": _split_tags(row["tags"]),
    }


def merchant_detail(row: sqlite3.Row) -> dict:
    """Full merchant shape used by get_merchant."""
    out = merchant_summary(row)
    out.update({
        "address": row["address"],
        "phone": row["phone"],
        "hours": row["hours"],
    })
    return out


def deal_view(row: sqlite3.Row) -> dict:
    return {
        "deal_id": row["deal_id"],
        "merchant_id": row["merchant_id"],
        "title": row["title"],
        "description": row["description"],
        "price_minor": int(row["price_minor"]),
        "list_price_minor": int(row["list_price_minor"]),
        "serves": int(row["serves"]),
        "valid_until": row["valid_until"],
        "status": row["status"],
    }


def _split_tags(raw) -> list:
    if not raw:
        return []
    return [t for t in str(raw).split(",") if t]
