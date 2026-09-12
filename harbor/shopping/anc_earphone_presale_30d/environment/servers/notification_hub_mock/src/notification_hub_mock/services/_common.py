"""Shared row-serialization helpers for services."""
import json
import sqlite3
from typing import Any, Optional


def _maybe_json(value: Optional[str]) -> Any:
    """Parse a JSON text column to a Python object, or return None.

    Falls back to the raw string if the column is non-JSON text.
    """
    if value is None:
        return None
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return value


def subscription_row(r: sqlite3.Row) -> dict:
    return {
        "subscription_id": r["subscription_id"],
        "user_id": r["user_id"],
        "source": r["source"],
        "type": r["type"],
        "target": r["target"],
        "condition": _maybe_json(r["condition_json"]),
        "status": r["status"],
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
    }


def notification_row(r: sqlite3.Row) -> dict:
    return {
        "notification_id": r["notification_id"],
        "user_id": r["user_id"],
        "source": r["source"],
        "type": r["type"],
        "subscription_id": r["subscription_id"],
        "title": r["title"],
        "body": r["body"],
        "payload": _maybe_json(r["payload_json"]),
        "created_at": r["created_at"],
        "read": bool(int(r["read"])),
    }


def price_alert_row(r: sqlite3.Row) -> dict:
    return {
        "alert_id": r["alert_id"],
        "user_id": r["user_id"],
        "item_ref": r["item_ref"],
        "target_price_minor": int(r["target_price_minor"]),
        "currency": r["currency"],
        "status": r["status"],
        "created_at": r["created_at"],
    }


def official_account_row(r: sqlite3.Row) -> dict:
    return {
        "account_id": r["account_id"],
        "name": r["name"],
        "category": r["category"],
        "description": r["description"],
    }


def post_row(r: sqlite3.Row) -> dict:
    return {
        "post_id": r["post_id"],
        "account_id": r["account_id"],
        "title": r["title"],
        "summary": r["summary"],
        "url": r["url"],
        "published_at": r["published_at"],
    }
