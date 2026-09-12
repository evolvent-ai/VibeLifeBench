"""Freeze the live triathlon world through the seven MCP services."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

USER_ID = "user_linz"
CLOCK = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
BASELINE = {
    "AGENTS.md", "BUDGET_AUTH.md", "HEALTH_BOUNDARIES.md", "IDENTITY.md",
    "PERSONA.md", "PRIVACY.md", "SOUL.md", "TOOLS.md",
    "TRAINING_PRINCIPLES.md", "USER.md",
}


class CaptureError(RuntimeError):
    pass


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value, fetch_page=None):
    """Return all rows from the canonical paginated envelope."""
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list):
        return value
    if "total" not in value and "has_more" not in value:
        return value
    merged = list(rows)
    total = value.get("total")
    total = int(total) if isinstance(total, (int, float)) else None
    page = int(value.get("page") or 1)
    current = value
    while fetch_page is not None and current.get("has_more"):
        page += 1
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            break
        fresh = nxt["items"]
        if not fresh:
            break
        merged.extend(fresh)
        current = nxt
        if total is not None and len(merged) >= total:
            break
    if total is not None and len(merged) < total:
        return {"items": merged, "_pagination_incomplete": True,
                "_captured": len(merged), "_total": total}
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        raise CaptureError(f"missing capability: {server}_mock")
    try:
        first = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            first,
            lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})),
        )
    except BaseException as exc:
        raise CaptureError(f"{server}.{tool}: {type(exc).__name__}: {exc}") from exc


def _email_page(env: Any, folder: str) -> dict[str, Any]:
    first = _call(env, "email", "get_emails", folder=folder, page=1, page_size=50)
    if not isinstance(first, dict):
        return {"listing": first, "details": {}}
    rows = list(first.get("emails") or [])
    total = int(first.get("total_results") or len(rows))
    page = 2
    seen = {str(r.get("email_id") or r.get("id")) for r in rows if isinstance(r, dict)}
    while len(rows) < total:
        nxt = _call(env, "email", "get_emails", folder=folder, page=page, page_size=50)
        if not isinstance(nxt, dict):
            break
        fresh = [r for r in (nxt.get("emails") or [])
                 if isinstance(r, dict) and str(r.get("email_id") or r.get("id")) not in seen]
        if not fresh:
            break
        rows.extend(fresh)
        seen.update(str(r.get("email_id") or r.get("id")) for r in fresh)
        page += 1
    first["emails"] = rows
    first["captured_complete"] = len(rows) >= total
    details = {}
    for row in rows:
        email_id = row.get("email_id") or row.get("id")
        if email_id is not None:
            details[str(email_id)] = _call(env, "email", "read_email", email_id=str(email_id))
    return {"listing": first, "details": details}


def _workspace(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    out: dict[str, str] = {}

    def walk(path: str, depth: int) -> None:
        name = path.rsplit("/", 1)[-1]
        if name.startswith(".") or name in BASELINE:
            return
        if name.lower().endswith((".md", ".txt", ".json", ".csv")):
            try:
                raw = fs.read_file(path)
                text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
                if text.strip():
                    out[path] = text[:200000]
            except Exception:
                pass
            return
        if depth:
            try:
                for child in fs.list_dir(path):
                    walk(f"{path.rstrip('/')}/{child}", depth - 1)
            except Exception:
                pass
    walk("/workspace", 4)
    return out


def capture_stage_snapshot(env: Any, stage: int) -> dict[str, Any]:
    clock = json.loads(CLOCK.read_text(encoding="utf-8"))
    if set(clock) != {"world_now"}:
        raise CaptureError("invalid world clock payload")
    parsed = datetime.fromisoformat(clock["world_now"].replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise CaptureError("world clock timestamp has no timezone")
    calendars = _call(env, "calendar", "list_calendars", user_id=USER_ID)
    calendar_ids = [str(r.get("calendar_id") or r.get("id")) for r in calendars
                    if isinstance(r, dict)] if isinstance(calendars, list) else []
    pages = _call(env, "notion", "API-post-search", query="", filter={"value": "page"}, page_size=100)
    page_rows = pages.get("results", []) if isinstance(pages, dict) else []
    merchant_search = {}
    merchant_ids = set()
    for category in ("pool", "cycling", "venue", "rental"):
        result = _call(env, "review_platform", "search_merchants", category=category, city="Hangzhou", limit=100)
        merchant_search[category] = result
        rows = result if isinstance(result, list) else result.get("items", []) if isinstance(result, dict) else []
        merchant_ids.update(str(r.get("merchant_id") or r.get("id")) for r in rows if isinstance(r, dict))
    products = {q: _call(env, "ecommerce", "search_products", query=q, limit=80)
                for q in ("gloves", "race-number belt", "helmet", "swimming goggles", "supplement", "bundle")}
    orders = _call(env, "ecommerce", "list_orders", user_id=USER_ID, limit=100)
    order_rows = orders if isinstance(orders, list) else orders.get("items", []) if isinstance(orders, dict) else []
    return {
        "stage": int(stage), "world_clock": clock, "workspace": _workspace(env),
        "calendar": {"calendars": calendars, "events": {cid: _call(env, "calendar", "list_events", calendar_id=cid, max_results=500) for cid in calendar_ids}},
        "health_tracker": {
            "metrics": {kind: _call(env, "health_tracker", "get_metrics", user_id=USER_ID, type=kind, limit=500) for kind in ("steps", "sleep_minutes", "heart_rate", "blood_pressure", "score")},
            "workouts": _call(env, "health_tracker", "list_workouts", user_id=USER_ID, limit=500),
            "goals": _call(env, "health_tracker", "get_goals", user_id=USER_ID),
        },
        "weather": {"alerts": _call(env, "weather", "get_alerts", geo="Hangzhou"), "daily": _call(env, "weather", "get_forecast_daily", geo="Hangzhou", days=14), "hourly": _call(env, "weather", "get_forecast_hourly", geo="Hangzhou", hours=120)},
        "notion": {"search": pages, "blocks": {str(p["id"]): _call(env, "notion", "API-get-block-children", block_id=str(p["id"])) for p in page_rows if isinstance(p, dict) and p.get("id")}},
        "email": {folder: _email_page(env, folder) for folder in ("INBOX", "Sent", "Drafts")},
        "ecommerce": {"products": products, "orders": orders, "order_details": {str(r.get("order_id") or r.get("id")): _call(env, "ecommerce", "get_order", order_id=str(r.get("order_id") or r.get("id"))) for r in order_rows if isinstance(r, dict) and (r.get("order_id") or r.get("id"))}, "cart": _call(env, "ecommerce", "get_cart", user_id=USER_ID)},
        "review_platform": {"search": merchant_search, "merchants": {mid: _call(env, "review_platform", "get_merchant", merchant_id=mid) for mid in merchant_ids}, "reviews": {mid: _call(env, "review_platform", "list_reviews", merchant_id=mid, limit=100) for mid in merchant_ids}, "reservations": _call(env, "review_platform", "list_reservations", user_id=USER_ID)},
    }
