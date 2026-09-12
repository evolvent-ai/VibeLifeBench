"""Freeze the constructor-examination world through its eleven MCP services."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

USER_ID = "user_lu_jing"
USER_EMAIL = "lu.jing@example.invalid"
CLOCK = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
BASELINE = {"AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}
CALENDAR_ID = "cal_primary_lu"


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value: Any, fetch_page=None) -> Any:
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list):
        return value
    if "total" not in value and "has_more" not in value:
        return value
    merged = list(rows)
    total_value = value.get("total")
    total = int(total_value) if isinstance(total_value, (int, float)) else None
    current, page = value, int(value.get("page") or 1)
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
    if (total is not None and len(merged) < total) or current.get("has_more"):
        return {"items": merged, "_pagination_incomplete": True,
                "_captured": len(merged), "_total": total}
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        first = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            first, lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})),
        )
    except BaseException as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


def _paged_call(env: Any, server: str, tool: str, *, rows_key: str,
                id_keys: tuple[str, ...], **kwargs: Any) -> Any:
    """Collect service-specific envelopes, notably email's clamped pages."""
    first = _call(env, server, tool, page=1, page_size=50, **kwargs)
    if not isinstance(first, dict) or first.get("error"):
        return first
    rows = list(first.get(rows_key) or [])
    total_value = first.get("total_results", first.get("total", len(rows)))
    total = int(total_value) if isinstance(total_value, (int, float)) else len(rows)

    def row_id(row: Any) -> str:
        if not isinstance(row, dict):
            return ""
        return next((str(row[key]) for key in id_keys if row.get(key) is not None), "")

    seen, page = {row_id(row) for row in rows}, 2
    while len(rows) < total:
        nxt = _call(env, server, tool, page=page, page_size=50, **kwargs)
        if not isinstance(nxt, dict) or nxt.get("error"):
            break
        fresh = [row for row in (nxt.get(rows_key) or []) if row_id(row) not in seen]
        if not fresh:
            break
        rows.extend(fresh)
        seen.update(row_id(row) for row in fresh)
        page += 1
    first[rows_key] = rows
    first["captured_count"] = len(rows)
    first["captured_complete"] = len(rows) >= total
    return first


def _email_folder(env: Any, folder: str, details: bool) -> dict[str, Any]:
    listing = _paged_call(env, "email", "get_emails", rows_key="emails",
                          id_keys=("email_id", "id"), folder=folder)
    captured = {}
    if details and isinstance(listing, dict):
        for row in listing.get("emails") or []:
            email_id = row.get("email_id") or row.get("id") if isinstance(row, dict) else None
            if email_id is None:
                continue
            detail = _call(env, "email", "read_email", email_id=str(email_id))
            headers = _call(env, "email", "get_email_headers", email_id=str(email_id))
            if isinstance(detail, dict) and isinstance(headers, dict):
                for key in ("in_reply_to", "references", "references_header", "headers", "thread_id"):
                    if headers.get(key) is not None:
                        detail.setdefault(key, headers[key])
            captured[str(email_id)] = detail
    return {"listing": listing, "details": captured}


def _workspace(env: Any) -> dict[str, str]:
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    out, seen = {}, set()

    def walk(path: str, depth: int) -> None:
        if path in seen or len(out) >= 200:
            return
        seen.add(path)
        name = path.rsplit("/", 1)[-1]
        if name.startswith(".") or name in BASELINE:
            return
        if name.lower().endswith((".md", ".txt", ".json", ".csv")):
            try:
                raw = fs.read_file(path)
            except Exception:  # noqa: BLE001
                return
            text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
            if text.strip():
                out[path] = text[:200000]
            return
        if depth:
            try:
                for child in fs.list_dir(path):
                    walk(f"{path.rstrip('/')}/{child}", depth - 1)
            except Exception:  # noqa: BLE001
                pass

    walk("/workspace", 4)
    return out


def _world_clock() -> dict[str, str]:
    payload = json.loads(CLOCK.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"world_now"}:
        raise RuntimeError("world clock must contain exactly world_now")
    value = payload["world_now"]
    if not isinstance(value, str):
        raise RuntimeError("world_now must be a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise RuntimeError("world_now must include a timezone")
    return {"world_now": value}


def _notion(env: Any) -> dict[str, Any]:
    search = _call(env, "notion", "API-post-search", query="", page_size=100)
    rows = search.get("results", []) if isinstance(search, dict) else []
    return {
        "search": search,
        "query_results": {q: _call(env, "notion", "API-post-search", query=q, page_size=100)
                          for q in ("FR9505", "380", "pine nut", "Luca")},
        "blocks": {str(row["id"]): _call(env, "notion", "API-get-block-children",
                                           block_id=str(row["id"]), page_size=100)
                   for row in rows if isinstance(row, dict) and row.get("id")},
    }


def capture_stage_snapshot(env: Any, stage_idx: int) -> dict[str, Any]:
    """Freeze every service slice used by the task rubric."""
    return {
        "stage": int(stage_idx), "world_clock": _world_clock(), "workspace": _workspace(env),
        "email": {"inbox": _email_folder(env, "INBOX", False), "sent": _email_folder(env, "Sent", True),
                   "drafts": _paged_call(env, "email", "get_drafts", rows_key="drafts", id_keys=("draft_id", "id"))},
        "calendar": {"events": _call(env, "calendar", "search_events", query="", max_results=500)},
        "notification_hub": {"subscriptions": _call(env, "notification_hub", "list_subscriptions", user_id=USER_ID),
                              "notifications": _call(env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500)},
        "content_platform": {"notes": {note_id: _call(env, "content_platform", "get_note", note_id=note_id)
                                          for note_id in ("note_zj_safety_duty_2026", "note_exam_integrity_risk", "note_ce_attendance_integrity")},
                              "collections": _call(env, "content_platform", "list_collections", user_id=USER_ID)},
        "ecommerce": {"products": _call(env, "ecommerce", "search_products", query="constructor", limit=100),
                       "orders": _call(env, "ecommerce", "list_orders", user_id=USER_ID),
                       "target_order": _call(env, "ecommerce", "get_order", order_id="order_20260706_4819")},
        "delivery_logistics": {"shipment": _call(env, "delivery_logistics", "get_shipment", shipment_id="ship_jd_260706_4819"),
                               "tracking": _call(env, "delivery_logistics", "track_package", tracking_no="JD-ZJ-260706-4819"),
                               "issues": _call(env, "delivery_logistics", "list_issues", user_id=USER_ID)},
        "maps": {"places": _call(env, "maps", "search_places", query="construction", city="Ningbo", limit=100),
                 "exam_site": _call(env, "maps", "get_place_details", place_id="place_nb_exam_haishu"),
                 "transit": _call(env, "maps", "get_transit", origin="Ningbo Station", dest="Ningbo Haishu Construction Examination Center", depart_at="2026-09-12T06:30:00+08:00")},
        "hotel_booking": {"hotels": _call(env, "hotel_booking", "search_hotels", city_or_geo="Ningbo", check_in="2026-09-11", check_out="2026-09-13", guests=1, filters={"limit": 50}),
                           "availability": _call(env, "hotel_booking", "get_room_availability", hotel_id="hotel_nb_hs_031", check_in="2026-09-11", check_out="2026-09-13", guests=1),
                           "reservations": _call(env, "hotel_booking", "list_reservations", user_id=USER_ID)},
        "rail_booking": {"trains": _call(env, "rail_booking", "search_trains", origin="Hangzhou", dest="Ningbo", date="2026-09-11", max_results=100),
                          "bookings": _call(env, "rail_booking", "list_train_bookings", user_id=USER_ID)},
        "weather": {"alerts": _call(env, "weather", "get_alerts", geo="Hangzhou"),
                    "forecast": _call(env, "weather", "get_forecast_daily", geo="Ningbo", days=10)},
        "notion": _notion(env),
    }
