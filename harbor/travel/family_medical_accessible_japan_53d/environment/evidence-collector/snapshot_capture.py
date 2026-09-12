"""Freeze the live accessible Kansai family trip world through its ten MCP services."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

USER_ID = "trav_liwei"
USER_EMAIL = "liwei@example.com"
CLOCK = Path(os.environ.get("WORLD_CLOCK_FILE", "/world-clock/current.json"))
BASELINE = {"AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md"}
FLIGHT_OFFERS = ("of_kansai_daytime_refundable_hold", "of_kansai_price_drop_20261008")


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
    flight_bookings = _call(env, "flight_booking", "list_bookings",
                            email=USER_EMAIL, page=1, page_size=50)
    booking_rows = flight_bookings.get("bookings", []) if isinstance(flight_bookings, dict) else flight_bookings
    hotel_ids = _call(env, "hotel_booking", "list_reservations", user_id=USER_ID)
    hotel_rows = hotel_ids.get("reservation_ids", []) if isinstance(hotel_ids, dict) else hotel_ids
    return {
        "stage": int(stage_idx), "world_clock": _world_clock(), "workspace": _workspace(env),
        "email": {
            "inbox": _email_folder(env, "INBOX", False),
            "sent": _email_folder(env, "Sent", True),
            "drafts": _paged_call(env, "email", "get_drafts", rows_key="drafts",
                                    id_keys=("draft_id", "id")),
        },
        "calendar": {"wedding_events": _call(
            env, "calendar", "search_events", query="Sofia Marco wedding",
            time_min="2026-09-12T00:00:00+02:00", time_max="2026-09-13T00:00:00+02:00",
            max_results=20)},
        "credit_card": {
            "cards": _call(env, "credit_card", "list_cards", user_id=USER_ID),
            "primary_card": _call(env, "credit_card", "get_card", card_id="card_travel_visa"),
        },
        "flight_booking": {
            "bookings": flight_bookings,
            "booking_details": {str(row["pnr"]): _call(env, "flight_booking", "get_booking",
                                                         pnr=str(row["pnr"]))
                                for row in (booking_rows or [])
                                if isinstance(row, dict) and row.get("pnr")},
            "offers": {offer_id: _call(env, "flight_booking", "get_flight_offer", offer_id=offer_id)
                       for offer_id in FLIGHT_OFFERS},
            "statuses": {
                "AZ608/2026-09-10": _call(env, "flight_booking", "get_flight_status",
                                            flight_no="AZ608", date="2026-09-10"),
                "UA971/2026-09-15": _call(env, "flight_booking", "get_flight_status",
                                            flight_no="UA971", date="2026-09-15"),
            },
        },
        "hotel_booking": {
            "reservation_ids": hotel_ids,
            "reservations": {str(rid): _call(env, "hotel_booking", "get_reservation",
                                               reservation_id=str(rid)) for rid in (hotel_rows or [])},
            "kyoto_availability": _call(
                env, "hotel_booking", "get_room_availability", hotel_id="jp_ht_001",
                check_in="2026-10-15", check_out="2026-10-16", guests=2),
        },
        "maps": {"accessible_routes": _call(env, "maps", "search_places", query="accessible Kyoto station elevator"),},
        "notion": _notion(env),
        "rail_booking": {
            "bookings": _call(env, "rail_booking", "list_train_bookings", user_id=USER_ID),
            "safe_offer": _call(env, "rail_booking", "search_trains", origin="Osaka",
                                 dest="Kyoto", date="2026-10-14", max_results=50),
            "maintenance": _call(env, "rail_booking", "get_train_status",
                                     train_no="A1738", date="2026-10-16"),
            "kansai_routes": _call(env, "rail_booking", "search_trains", origin="Kyoto",
                                     dest="Nara", date="2026-10-16", max_results=50),
        },
        "visa_and_advisory": {
            "entry": _call(env, "visa_and_advisory", "check_entry_requirements",
                                 nationality="CN", destination="JP", purpose="tourism", transit_countries=[]),
            "passports": _call(env, "visa_and_advisory", "list_visa_applications", user_id=USER_ID),
        },
        "weather": {"alerts": _call(env, "weather", "get_alerts", geo="kyoto"),
                    "forecast": _call(env, "weather", "get_forecast_daily", geo="kyoto", days=7)},
    }
