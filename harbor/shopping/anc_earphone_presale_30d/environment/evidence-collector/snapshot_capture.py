"""Authoritative stage snapshots for the ANC presale environment."""
from __future__ import annotations
import json, os, sqlite3
from pathlib import Path
from typing import Any

WORLD_CLOCK_FILE = os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json")

DB_PATHS = {
    "calendar": "/calendar-env/runtime.db",
    "credit_card": "/credit-card-env/runtime.db",
    "delivery_logistics": "/delivery-logistics-env/runtime.db",
    "ecommerce": "/ecommerce-env/runtime.db",
    "email": "/email-env/runtime.db",
    "listing_platform": "/listing-platform-env/runtime.db",
    "notification_hub": "/notification-hub-env/runtime.db",
    "weather": "/weather-env/runtime.db",
}

def scenario_clock() -> dict[str, Any]:
    payload = json.loads(Path(WORLD_CLOCK_FILE).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"world_now"}:
        raise RuntimeError("world clock must contain exactly world_now")
    return {"schema_version": 1, "now": payload["world_now"]}

def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    return value

def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict): return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value): return value
    merged = list(rows)
    page = int(value.get("page") or 1) + 1
    total = int(value.get("total") or 0)
    while value.get("has_more") and fetch_page is not None and (not total or len(merged) < total):
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            value["_pagination_incomplete"] = True; break
        merged.extend(nxt["items"]); value = nxt; page += 1
    if value.get("has_more"): value["_pagination_incomplete"] = True
    return merged

def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None: return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(value, lambda p: _decode(cap.call_tool(tool, **{**kwargs, "page": p})))
    except BaseException as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def _raw_rows(server: str, table: str) -> list[dict[str, Any]]:
    """Read immutable backend rows for fields not exposed by list tools.

    The sidecar is trusted capture code and the database volumes are read-only
    from the scorer.  Keeping these rows in the frozen snapshot prevents a
    public summary endpoint from silently dropping refund, SKU, or ledger
    details required by the historical rubrics.
    """
    path = DB_PATHS.get(server)
    if not path or not os.path.isfile(path):
        return []
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        rows = [dict(row) for row in conn.execute(f"SELECT * FROM {table}")]
        conn.close()
    except Exception:
        return []
    return rows


def _parse_json_columns(row: dict[str, Any]) -> dict[str, Any]:
    for key, value in list(row.items()):
        if key.endswith("_json") and isinstance(value, str):
            try:
                row[key] = json.loads(value)
            except json.JSONDecodeError:
                pass
    return row


def _calendar_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["start"] = {"dateTime": row.get("start_dt")}
        row["end"] = {"dateTime": row.get("end_dt")}
    return rows


def _enrich_email(payload: Any) -> Any:
    raw = {_row.get("id"): _row for _row in _raw_rows("email", "messages")}
    if not isinstance(payload, dict):
        return payload
    for page in (payload.get("inbox"), payload.get("sent")):
        if not isinstance(page, dict):
            continue
        for item in page.get("emails") or []:
            try:
                detail = raw.get(int(item.get("email_id")))
            except (TypeError, ValueError):
                detail = None
            if detail:
                item["id"] = detail.get("id")
                item["body_text"] = detail.get("body_text") or ""
                item["headers_json"] = detail.get("headers_json") or "{}"
    return payload


def _enrich_notifications(payload: Any) -> Any:
    raw = {_row.get("notification_id"): _row for _row in _raw_rows("notification_hub", "notifications")}
    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            detail = raw.get(item.get("notification_id"))
            if detail:
                item["payload_json"] = detail.get("payload_json") or "{}"
    return payload


def _normalize_calendar(payload: Any) -> Any:
    aliases = {
        "信用卡还款日": "credit card payment due date",
        "尾款举证截止": "final-payment evidence deadline",
        "资金台账复核": "funds-ledger review",
    }
    if isinstance(payload, list):
        for row in payload:
            if isinstance(row, dict):
                row["summary"] = aliases.get(row.get("summary"), row.get("summary"))
    return payload

def _workspace_snapshot(env: Any) -> dict[str, Any]:
    files = {}
    for name in env.workspace.fs.list_dir("/workspace"):
        path = f"/workspace/{name}"
        if name.endswith((".md", ".txt", ".json", ".csv")) and env.workspace.fs.exists(path):
            try: files[name] = env.workspace.fs.read_file(path).decode("utf-8", "replace")
            except Exception: pass
    return {"files": files}

def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    ecommerce_orders = _call(env, "ecommerce", "list_orders", user_id="usr_teng_qi", limit=100)
    ecommerce_products = _call(env, "ecommerce", "search_products", query="SonicPod", limit=100)
    calendar_events = _normalize_calendar(_call(env, "calendar", "list_events", max_results=500))
    if isinstance(calendar_events, list):
        for row in calendar_events:
            if isinstance(row, dict):
                start = row.get("start") or {}
                end = row.get("end") or {}
                row["start_dt"] = start.get("dateTime") or start.get("date")
                row["end_dt"] = end.get("dateTime") or end.get("date")
    inbox = _enrich_email(_call(env, "email", "get_emails", folder="INBOX", page=1, page_size=200))
    sent = _enrich_email(_call(env, "email", "get_emails", folder="Sent", page=1, page_size=200))
    # Keep a flat, authoritative message projection as well as the service's
    # folder envelopes.  Rubrics address messages by Message-ID and need the
    # full body/header fields from the immutable backend rows.
    email_messages = [_parse_json_columns(r) for r in _raw_rows("email", "messages")]
    notifications = _enrich_notifications(_call(env, "notification_hub", "list_notifications", user_id="usr_teng_qi", limit=500))
    official_posts = [_parse_json_columns(r) for r in _raw_rows("notification_hub", "official_account_posts")]
    listing_rows = [_parse_json_columns(r) for r in _raw_rows("listing_platform", "listings")]
    if not listing_rows:
        listing_rows = _call(env, "listing_platform", "search_listings", category="secondhand", keyword="SonicPod", limit=100)
    ecommerce = {
        "orders": ecommerce_orders,
        "products": ecommerce_products,
        "skus": [_parse_json_columns(r) for r in _raw_rows("ecommerce", "skus")],
        "stocks": [_parse_json_columns(r) for r in _raw_rows("ecommerce", "stocks")],
        "coupons": [_parse_json_columns(r) for r in _raw_rows("ecommerce", "coupons")],
        "cart_items": [_parse_json_columns(r) for r in _raw_rows("ecommerce", "cart_items")],
        "refunds": [_parse_json_columns(r) for r in _raw_rows("ecommerce", "refunds")],
    }
    credit_card = {
        "cards": _call(env, "credit_card", "list_cards", user_id="usr_teng_qi"),
        "unbilled_transactions": [_parse_json_columns(r) for r in _raw_rows("credit_card", "unbilled_transactions")],
        "disputes": [_parse_json_columns(r) for r in _raw_rows("credit_card", "disputes")],
    }
    weather = {
        "locations": _call(env, "weather", "get_current_weather", geo="geo_psea"),
        "daily": _call(env, "weather", "get_forecast_daily", geo="geo_psea", days=14),
        "daily_weather": [_parse_json_columns(r) for r in _raw_rows("weather", "daily_weather")],
        "daily_aqi": [_parse_json_columns(r) for r in _raw_rows("weather", "daily_aqi")],
        "alerts": [_parse_json_columns(r) for r in _raw_rows("weather", "alerts")],
        "notifications": [_parse_json_columns(r) for r in _raw_rows("weather", "notifications")],
    }
    return {
        "stage": stage_idx, "scenario_clock": scenario_clock(),
        "ecommerce": ecommerce,
        "delivery_logistics": {"shipments": _call(env, "delivery_logistics", "list_shipments", user_id="usr_teng_qi", limit=100)},
        "credit_card": credit_card,
        "email": {"messages": email_messages, "inbox": inbox, "sent": sent},
        "calendar": {"events": calendar_events},
        "notification_hub": {"subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id="usr_teng_qi"), "notifications": notifications, "official_account_posts": official_posts},
        "listing_platform": {"listings": listing_rows},
        "weather": weather,
        "workspace": _workspace_snapshot(env),
    }
