"""Shared Harbor-native evidence helpers for the Bali trip rubric."""
from __future__ import annotations

import json
from typing import Any

from harbor_evidence import response as evidence_response
from harbor_evidence import snapshot as evidence_snapshot
from harbor_evidence import trace as evidence_trace

RESPONSES_DIR = "/terrarium/agent_responses"
TRACE_DIR = "/terrarium/agent_traces"
STAGE_COUNT = 24


def snapshot(env, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env, stage: int) -> str:
    return env.response(stage)


def _active_stage(env) -> int:
    value = getattr(env, "active_stage", None)
    if value is not None:
        return int(value)
    stages = env.published_stages()
    if not stages:
        raise RuntimeError("rubric requires published frozen evidence")
    return max(stages)


def _as_obj(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="strict")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(_flatten(v) for v in value.values())
    if isinstance(value, (list, tuple, set)):
        return " ".join(_flatten(v) for v in value)
    return str(value)


def _section(env, server: str) -> dict[str, Any]:
    section = snapshot(env, _active_stage(env)).get(server)
    if not isinstance(section, dict):
        raise RuntimeError(f"frozen snapshot has no {server!r} projection")
    return section


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    value = _as_obj(value)
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in keys:
            candidate = value.get(key)
            if isinstance(candidate, list):
                return [row for row in candidate if isinstance(row, dict)]
    return []


def _find(rows: list[dict[str, Any]], keys: tuple[str, ...], wanted: str) -> dict[str, Any] | None:
    for row in rows:
        for key in keys:
            if str(row.get(key) or "").casefold() == wanted.casefold():
                return row
    return None


def _trace_result(env, server: str, tool: str, kwargs: dict[str, Any]) -> Any:
    """Return a matching successful call result when the snapshot has no projection."""
    for call in _tool_calls(env):
        if not _tool_name_matches(str(call.get("name") or ""), server, tool):
            continue
        args = call.get("arguments")
        if isinstance(args, dict) and any(str(args.get(k)) != str(v) for k, v in kwargs.items() if k in args):
            continue
        if "result" in call:
            return _as_obj(call.get("result"))
    return None


def _call(env, server: str, tool: str, **kwargs: Any):
    """Read one historical backend projection from the immutable snapshot."""
    section = _section(env, server)
    if server == "flight_booking":
        bookings = _rows(section.get("bookings"), "bookings")
        if tool == "list_bookings":
            return section.get("bookings", [])
        if tool == "get_booking":
            return _find(bookings, ("pnr", "booking_id"), str(kwargs.get("pnr") or ""))
        if tool in {"get_flight_status", "get_status"}:
            statuses = section.get("flight_status") or section.get("statuses") or []
            if isinstance(statuses, dict):
                key = f"{kwargs.get('flight_no')}:{kwargs.get('date')}"
                if key in statuses:
                    return statuses[key]
                if statuses:
                    return statuses
            elif statuses:
                return statuses
    elif server == "hotel_booking":
        reservations = _rows(section.get("reservations"), "reservations")
        if tool == "list_reservations":
            return section.get("reservations", [])
        if tool == "get_reservation":
            return _find(reservations, ("reservation_id", "id"), str(kwargs.get("reservation_id") or ""))
        if tool == "get_hotel_details":
            details = section.get("hotel_details") or section.get("hotels") or []
            if isinstance(details, dict):
                wanted = str(kwargs.get("hotel_id") or "")
                if wanted in details:
                    return details[wanted]
                if details.get("hotel_id") or details.get("property_id"):
                    return details
            else:
                found = _find(_rows(details, "hotels"), ("hotel_id", "property_id", "id"), str(kwargs.get("hotel_id") or ""))
                if found is not None:
                    return found
    elif server == "calendar":
        events = _rows(section.get("events"), "events")
        if tool in {"list_events", "search_events"}:
            query = str(kwargs.get("query") or "").casefold()
            if query:
                events = [row for row in events if query in _flatten(row).casefold()]
            return events
        if tool == "list_calendars":
            return section.get("calendars", [])
    elif server == "notion":
        if tool == "API-post-search":
            pages = section.get("pages") or section.get("search") or []
            rows = pages.get("results", []) if isinstance(pages, dict) else pages
            query = str(kwargs.get("query") or "").casefold()
            if query:
                rows = [row for row in rows if query in _flatten(row).casefold()]
            return {"results": rows} if isinstance(pages, dict) else rows
        if tool == "API-get-block-children":
            blocks = section.get("page_blocks") or section.get("blocks") or {}
            value = blocks.get(str(kwargs.get("block_id") or ""), []) if isinstance(blocks, dict) else []
            return value if isinstance(value, dict) else {"results": value}
        if tool == "API-post-database-query":
            rows = section.get("database_rows") or {}
            return rows.get(str(kwargs.get("database_id") or ""), []) if isinstance(rows, dict) else rows
    elif server == "visa_and_advisory":
        if tool == "get_advisory":
            return section.get("advisories", {})
        apps = _rows(section.get("applications"), "applications")
        if tool == "list_visa_applications":
            return section.get("applications", [])
        if tool == "get_visa_application":
            found = _find(apps, ("application_id", "id"), str(kwargs.get("application_id") or ""))
            if found is not None:
                return found
        if tool == "check_entry_requirements":
            requirements = section.get("entry_requirements")
            if requirements:
                return requirements
    elif server == "weather":
        if tool == "get_alerts":
            alerts = section.get("alerts", [])
            if "dps" in str(kwargs.get("geo") or "").casefold() or "kintamani" in _flatten(alerts).casefold() or "ubud" in _flatten(alerts).casefold():
                return alerts
        if tool.startswith("get_forecast"):
            key = "forecast_ubud" if "ubud" in str(kwargs.get("geo")) else "forecast_kintamani"
            return section.get(key, [])
    elif server == "maps":
        if tool == "search_places":
            return section.get("places", [])
        if tool == "get_place_details":
            found = _find(_rows(section.get("places"), "places"), ("place_id", "id"), str(kwargs.get("place_id") or ""))
            if found is not None:
                return found
        if tool == "get_traffic_estimate":
            traffic = section.get("traffic", {})
            if traffic:
                return traffic
        if tool in {"directions", "distance_matrix"}:
            directions = section.get("directions", {})
            if directions:
                return directions
    elif server == "email":
        folder = str(kwargs.get("folder") or "INBOX").casefold()
        key = "sent" if folder in {"sent", "sent items", "inbox.sent"} else "inbox"
        payload = section.get(key, [])
        listing = payload.get("listing", payload) if isinstance(payload, dict) else payload
        details = payload.get("details", []) if isinstance(payload, dict) else []
        messages = _rows(listing, "messages", "emails")
        if tool in {"get_emails", "search_emails"}:
            query = str(kwargs.get("query") or "").casefold()
            if query:
                messages = [row for row in messages if query in _flatten(row).casefold()]
            return {"emails": messages}
        if tool == "read_email":
            return _find(messages + _rows(details), ("email_id", "id"), str(kwargs.get("email_id") or ""))
        if tool == "get_email_headers":
            return _find(_rows(details), ("email_id", "id"), str(kwargs.get("email_id") or "")) or {}
        if tool == "get_drafts":
            return section.get("drafts", [])
    traced = _trace_result(env, server, tool, kwargs)
    if traced is not None:
        return traced
    raise RuntimeError(f"unsupported frozen backend projection: {server}.{tool}")


def _tool_calls(env, stage: int | None = None) -> list[dict[str, Any]]:
    stages = [stage] if stage is not None else list(range(STAGE_COUNT))
    published = set(env.published_stages())
    calls: list[dict[str, Any]] = []
    for idx in stages:
        if stage is None and idx not in published:
            continue
        rows = trace(env, idx)
        if not isinstance(rows, list):
            raise RuntimeError(f"frozen trace for stage {idx} is not a list")
        calls.extend(row for row in rows if isinstance(row, dict) and row.get("success") is True)
    return calls


def _tool_name_matches(name: str, server: str, tool: str) -> bool:
    norm = str(name or "").casefold().replace("-", "_")
    server_norm = server.casefold().replace("-", "_")
    tool_norm = tool.casefold().replace("-", "_")
    return norm == tool_norm or norm == f"{server_norm}__{tool_norm}" or norm == f"{server_norm}_{tool_norm}" or norm.endswith(f"__{tool_norm}")


def _tool_call_matches(env, server: str, tool: str, predicate, *, stage: int) -> bool:
    for call in _tool_calls(env, stage):
        if _tool_name_matches(str(call.get("name") or ""), server, tool):
            args = call.get("arguments")
            if isinstance(args, dict) and predicate(args):
                return True
    return False


def list_flight_bookings(env) -> list[dict]:
    result = _call(env, "flight_booking", "list_bookings", page=1, page_size=50)
    rows = _rows(result, "bookings")
    expanded = []
    for row in rows:
        pnr = str(row.get("pnr") or "").strip()
        if not pnr:
            raise ValueError("flight booking summary is missing pnr")
        detail = get_flight_booking(env, pnr)
        if not isinstance(detail, dict):
            raise ValueError(f"flight booking detail missing for {pnr}")
        expanded.append({**row, **detail})
    return expanded


def get_flight_booking(env, pnr: str) -> dict | None:
    return _call(env, "flight_booking", "get_booking", pnr=pnr)


def list_hotel_reservations(env) -> list[dict]:
    result = _call(env, "hotel_booking", "list_reservations", user_id="usr_chen_yu")
    raw = _as_obj(result)
    if isinstance(raw, dict) and isinstance(raw.get("reservation_ids"), list):
        rows = [{"reservation_id": rid} for rid in raw["reservation_ids"] if rid]
    else:
        rows = _rows(raw, "reservations")
    expanded = []
    for row in rows:
        rid = str(row.get("reservation_id") or row.get("id") or "").strip()
        if not rid:
            raise ValueError("hotel reservation summary is missing reservation_id")
        detail = get_hotel_reservation(env, rid)
        if not isinstance(detail, dict):
            raise ValueError(f"hotel reservation detail missing for {rid}")
        expanded.append({**row, **detail})
    return expanded


def get_hotel_reservation(env, reservation_id: str) -> dict | None:
    return _call(env, "hotel_booking", "get_reservation", reservation_id=reservation_id)


def search_calendar_events(env, query: str) -> list[dict]:
    return _rows(_call(env, "calendar", "search_events", query=query), "events")


def notion_search(env, query: str) -> list[dict]:
    return _rows(_call(env, "notion", "API-post-search", query=query), "results")


def notion_get_blocks(env, page_id: str) -> list[dict]:
    return _rows(_call(env, "notion", "API-get-block-children", block_id=page_id), "results")


def notion_page_text(env) -> str:
    pages = notion_search(env, "Bali Trip 2026")
    if not pages:
        return ""
    page_id = pages[0].get("id")
    blocks = notion_get_blocks(env, str(page_id)) if page_id else []
    text: list[str] = []
    for block in blocks:
        btype = str(block.get("type") or "")
        payload = block.get(btype, {})
        for segment in payload.get("rich_text", []) if isinstance(payload, dict) else []:
            if isinstance(segment, dict):
                value = segment.get("plain_text") or (segment.get("text") or {}).get("content", "")
                if value:
                    text.append(str(value))
    return "\n".join(text)


def workspace_file_content(env, path: str) -> str:
    snap = snapshot(env, _active_stage(env))
    workspace = snap.get("workspace", {})
    if not isinstance(workspace, dict):
        raise RuntimeError("frozen snapshot has no workspace projection")
    value = workspace.get(path)
    if value is None:
        suffix = path.rsplit("/", 1)[-1]
        matches = [v for k, v in workspace.items() if str(k).rsplit("/", 1)[-1] == suffix]
        if len(matches) == 1:
            value = matches[0]
    return value.decode("utf-8", errors="strict") if isinstance(value, bytes) else str(value or "")


def _agent_responses(env, stage: int) -> str:
    return evidence_response(env, stage)


def _money(record: dict, *keys: str, default_currency: str) -> tuple[float, str]:
    for key in keys:
        value = record.get(key)
        if value is None:
            continue
        if isinstance(value, dict):
            amount = value.get("amount")
            currency = value.get("currency") or record.get("currency") or default_currency
        else:
            amount = value
            currency = record.get("currency") or default_currency
        if amount is not None:
            return float(amount), str(currency).upper()
    return 0.0, default_currency


def compute_total_spend_cny(env) -> float:
    total = 0.0
    for booking in list_flight_bookings(env):
        if str(booking.get("status") or "").upper() in {"CANCELLED", "CANCELED"}:
            continue
        amount, currency = _money(booking, "total_paid", "total_price", "price", "amount", default_currency="CNY")
        total += amount / 2200.0 if currency == "IDR" else amount
    for reservation in list_hotel_reservations(env):
        if str(reservation.get("status") or "").upper() in {"CANCELLED", "CANCELED", "WALKED", "CHECKED_OUT"}:
            continue
        amount, currency = _money(reservation, "total_charged", "total_price", "total", "amount", default_currency="IDR")
        total += amount / 2200.0 if currency == "IDR" else amount
    return total
