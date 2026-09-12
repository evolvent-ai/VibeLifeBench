"""Shared rubric helper functions for east_asia_group_trip_24d.

Import from ._helpers in each stage_<N>.py, final.py, and cross_stage.py.
"""
from __future__ import annotations

import json
import re
from typing import Any

from harbor_evidence import HarborEvidence, snapshot as _evidence_snapshot
from harbor_evidence import trace as _evidence_trace
from harbor_evidence import response as _evidence_response

OUTPUT_PATHS = (
    "/workspace/profiles.md",
    "/workspace/flights.md",
    "/workspace/hotels.md",
    "/workspace/budget.md",
    "/workspace/bookings.md",
    "/workspace/itinerary.md",
    "/workspace/risk_register.md",
    "/workspace/health_watch.md",
    "/workspace/decision_log.md",
    "/workspace/incident_log.md",
)

STAGE_COUNT = 22
NOTION_PAGE_TITLE = "East Asia Group Trip 2026 - Journal"


# ── Harbor evidence access ────────────────────────────────────────────────

def snapshot(env: HarborEvidence, stage: int) -> dict[str, Any]:
    return _evidence_snapshot(env, stage)


def trace(env: HarborEvidence, stage: int) -> list[dict[str, Any]]:
    return _evidence_trace(env, stage)


def response(env: HarborEvidence, stage: int) -> str:
    return _evidence_response(env, stage)


def _current_stage(env: HarborEvidence) -> int:
    return int(getattr(env, "current_stage", getattr(env, "virtual_stage", 0)))


def _decode_result(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    if isinstance(value, list) and value:
        text_blocks = [
            item.get("text") or item.get("content")
            for item in value
            if isinstance(item, dict) and (item.get("text") is not None or item.get("content") is not None)
        ]
        if len(text_blocks) == 1:
            return _decode_result(text_blocks[0])
    if isinstance(value, dict):
        structured = value.get("structuredContent") or value.get("structured_content")
        if isinstance(structured, dict) and "result" in structured:
            return _decode_result(structured["result"])
    return value


def _trace_call_result(env, server: str, tool: str, kwargs: dict[str, Any]) -> Any:
    """Return the matching recorded tool result, if this stage recorded one."""
    current = _current_stage(env)
    published = env.published_stages() if hasattr(env, "published_stages") else [current]
    stages = [current, *sorted((stage for stage in published if stage < current), reverse=True)]
    for stage in dict.fromkeys(stages):
        for call in trace(env, stage):
            name = str(call.get("name") or call.get("tool") or "")
            if not _tool_name_matches(name, server, tool):
                continue
            args = call.get("arguments") or call.get("args") or {}
            if isinstance(args, dict) and all(args.get(k) == v for k, v in kwargs.items()):
                if call.get("success") is not True:
                    continue
                return _decode_result(call.get("result"))
    return None


def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    """Resolve a former service read from the frozen snapshot or trace.

    Agent-issued reads are preferred because they preserve the exact payload
    for transient APIs. Durable backend state comes from the stage snapshot.
    """
    traced = _trace_call_result(env, server, tool, kwargs)
    if traced is not None:
        return traced
    state = snapshot(env, _current_stage(env))
    section = state.get(server, {}) if isinstance(state, dict) else {}
    if not isinstance(section, dict):
        return {}

    if server == "flight_booking":
        if tool == "list_bookings":
            return section.get("bookings", [])
        if tool == "get_booking":
            details = section.get("booking_details", {})
            return details.get(str(kwargs.get("pnr")), {}) if isinstance(details, dict) else {}
        if tool == "get_flight_status":
            bookings = section.get("booking_details", {})
            for booking in bookings.values() if isinstance(bookings, dict) else []:
                for segment in booking.get("segments", []) if isinstance(booking, dict) else []:
                    if (str(segment.get("flight_no") or "").replace(" ", "").upper()
                            == str(kwargs.get("flight_no") or "").replace(" ", "").upper()
                            and str(segment.get("depart_dt") or "")[:10] == str(kwargs.get("date") or "")):
                        return {**segment, "flight_no": kwargs.get("flight_no"), "date": kwargs.get("date"),
                                "status": booking.get("status")}
            return {}
    elif server == "hotel_booking":
        if tool == "list_reservations":
            return section.get("reservations", [])
        details = section.get("reservation_details", {})
        if tool == "get_reservation" and isinstance(details, dict):
            return details.get(str(kwargs.get("reservation_id")), {})
        if tool == "get_hotel_details" and isinstance(details, dict):
            for reservation in details.values():
                if isinstance(reservation, dict) and str(reservation.get("hotel_id")) == str(kwargs.get("hotel_id")):
                    return reservation.get("hotel", reservation)
    elif server == "visa_and_advisory":
        if tool == "check_entry_requirements" and kwargs.get("destination") == "JP":
            return section.get("entry_requirements", {})
        if tool == "get_advisory" and kwargs.get("country_code") == "JP":
            return section.get("advisory", {})
        if tool == "list_visa_applications":
            return section.get("applications", [])
        if tool == "get_visa_application":
            details = section.get("application_details", {})
            return details.get(str(kwargs.get("application_id")), {}) if isinstance(details, dict) else {}
    elif server == "notion":
        notion = section
        if tool in {"API-post-search", "api-post-search"}:
            return notion.get("search", {})
        if tool == "API-get-block-children":
            blocks = notion.get("blocks", {})
            return blocks.get(str(kwargs.get("block_id")), {}) if isinstance(blocks, dict) else {}
        if tool == "API-retrieve-a-page":
            for page in notion.get("pages", []) if isinstance(notion.get("pages"), list) else []:
                if str(page.get("id")) == str(kwargs.get("page_id")):
                    return page
    elif server == "calendar" and tool == "list_events":
        return section.get("events", [])
    elif server == "email":
        if tool in {"search_emails", "get_emails"}:
            inbox = section.get("inbox", {})
            return inbox.get("listing", inbox) if isinstance(inbox, dict) else inbox
        if tool == "read_email":
            email_id = str(kwargs.get("email_id"))
            for folder in ("inbox", "sent"):
                details = section.get(folder, {}).get("details", {})
                if isinstance(details, dict) and email_id in details:
                    return details[email_id]
    elif server == "banking":
        if tool == "get_account":
            return section.get("account", {})
        if tool == "list_transactions":
            return section.get("transactions", [])
    elif server == "health_tracker":
        if tool == "get_goals":
            return section.get("goals", [])
        if tool == "get_metrics":
            return section.get("metrics", [])
        if tool == "get_latest_metric":
            metrics = section.get("metrics", [])
            rows = (metrics.get("metrics") or metrics.get("items") or []) if isinstance(metrics, dict) else metrics
            if isinstance(rows, list) and rows:
                return rows[-1]
            alerts = _call(env, "health_tracker", "list_health_alerts", user_id=kwargs.get("user_id"))
            alert_rows = (alerts.get("alerts") or alerts.get("items") or []) if isinstance(alerts, dict) else alerts
            if isinstance(alert_rows, list) and alert_rows:
                alert = alert_rows[0]
                if isinstance(alert, dict):
                    return {**alert, "user_id": kwargs.get("user_id")}
    return {}


# ── text helpers ───────────────────────────────────────────────────────────

def _flatten_text(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float, bool)):
        return str(obj)
    if isinstance(obj, list):
        return "\n".join(_flatten_text(x) for x in obj)
    if isinstance(obj, dict):
        return "\n".join(_flatten_text(v) for v in obj.values())
    return ""


def _any(text: str, words: list[str]) -> bool:
    if not text:
        return False
    return any(w.lower() in text for w in words)


def _count_any(text: str, words: list[str]) -> int:
    if not text:
        return 0
    return sum(1 for w in words if w.lower() in text)


def _number_count(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(r"(?<!\d)\d+(?:,\d{3})*(?:\.\d+)?(?!\d)", text))


# ── workspace file helpers ─────────────────────────────────────────────────

def _workspace_file_text(env, path: str) -> str:
    workspace = snapshot(env, _current_stage(env)).get("workspace", {})
    if isinstance(workspace, dict):
        if path in workspace:
            return str(workspace[path])
        base = path.rsplit("/", 1)[-1]
        for candidate, value in workspace.items():
            if str(candidate).rstrip("/").rsplit("/", 1)[-1] == base:
                return str(value)
    return ""


def _workspace_text(env) -> str:
    chunks: list[str] = []
    for path in OUTPUT_PATHS:
        body = _workspace_file_text(env, path)
        if body:
            chunks.append(body)
    return "\n".join(chunks)


# ── agent response helpers ─────────────────────────────────────────────────

def _agent_response(env, idx: int) -> str:
    return response(env, idx)


# ── Notion helpers ─────────────────────────────────────────────────────────

def _notion_text(env) -> str:
    search = _call(env, "notion", "API-post-search", query=NOTION_PAGE_TITLE,
                   filter={"value": "page"}, page_size=10)
    pages: list[dict] = []
    if isinstance(search, dict):
        pages = [p for p in search.get("results") or [] if isinstance(p, dict)]
    if not pages:
        return ""

    chunks: list[str] = []
    for page in pages[:3]:
        page_id = page.get("id")
        chunks.append(_flatten_text(page))
        if not page_id:
            continue
        children = _call(env, "notion", "API-get-block-children", block_id=page_id)
        chunks.append(_flatten_text(children))
    return "\n".join(chunks)


def _notion_page_count(env) -> int:
    search = _call(
        env,
        "notion",
        "API-post-search",
        query=NOTION_PAGE_TITLE,
        filter={"value": "page"},
        page_size=10,
    )
    pages: list[dict] = []
    if isinstance(search, dict):
        pages = [p for p in search.get("results") or [] if isinstance(p, dict)]
    return len(pages)


def _notion_block_count(env) -> int:
    search = _call(
        env,
        "notion",
        "API-post-search",
        query=NOTION_PAGE_TITLE,
        filter={"value": "page"},
        page_size=10,
    )
    pages: list[dict] = []
    if isinstance(search, dict):
        pages = [p for p in search.get("results") or [] if isinstance(p, dict)]
    if not pages:
        return 0
    block_count = 0
    for page in pages[:3]:
        page_id = page.get("id")
        if not page_id:
            continue
        children = _call(env, "notion", "API-get-block-children", block_id=page_id)
        if isinstance(children, dict):
            results = children.get("results") or []
            block_count += len(results)
    return block_count


# ── corpus functions ───────────────────────────────────────────────────────

def _stage_corpus(env, idx: int) -> str:
    return "\n".join([
        _agent_response(env, idx),
        _workspace_text(env),
        _notion_text(env),
    ]).lower()


# ── tool-call trace analysis ───────────────────────────────────────────────

def _tool_calls(env, stage: int | None = None, *, include_failed: bool = False) -> list[dict[str, Any]]:
    if stage is not None:
        stages = [stage]
    elif hasattr(env, "published_stages"):
        stages = env.published_stages()
    else:
        stages = list(range(STAGE_COUNT))
    calls: list[dict[str, Any]] = []
    for idx in stages:
        parsed = trace(env, idx)
        if not isinstance(parsed, list):
            raise ValueError(f"rubric trace must be a list for stage {idx}")
        calls.extend(c for c in parsed if isinstance(c, dict) and (include_failed or c.get("success") is True))
    return calls


def _tool_result_text(call: dict[str, Any]) -> str:
    return str(call.get("result") or "").lower()


def _successful_email_read(
    env,
    stage: int,
    required_terms: tuple[str, ...],
    *,
    from_addr: str,
) -> dict[str, Any] | None:
    """Return a full email object that the agent successfully read at ``stage``."""
    expected_sender = from_addr.casefold()
    expected_terms = tuple(term.casefold() for term in required_terms)
    for call in _tool_calls(env, stage):
        if not _tool_name_matches(str(call.get("name") or ""), "email", "read_email"):
            continue
        args = call.get("arguments") if isinstance(call.get("arguments"), dict) else {}
        email_id = args.get("email_id")
        detail = _decode_result(call.get("result"))
        if email_id is None or not isinstance(detail, dict):
            continue
        returned_id = detail.get("email_id") or detail.get("id")
        if str(returned_id or "") != str(email_id):
            continue
        if str(detail.get("from_addr") or "").casefold() != expected_sender:
            continue
        blob = _flatten_text(detail).casefold()
        if all(term in blob for term in expected_terms):
            return detail
    return None


def _tool_name_matches(name: str, server: str | None = None, tool: str | None = None) -> bool:
    norm = (name or "").lower().replace("-", "_")
    if server:
        server_norm = server.lower().replace("-", "_")
        if not (norm.startswith(f"{server_norm}__") or norm.startswith(f"{server_norm}_")):
            return False
    if tool:
        tool_norm = tool.lower().replace("-", "_")
        return norm == tool_norm or norm.endswith(f"__{tool_norm}") or norm.endswith(f"_{tool_norm}")
    return bool(norm)


def _agent_used_tool(
    env,
    server: str | None = None,
    tool: str | None = None,
    *,
    stage: int | None = None,
) -> bool:
    return any(
        _tool_name_matches(str(call.get("name") or ""), server, tool)
        for call in _tool_calls(env, stage)
    )


def _agent_used_any_tool(
    env,
    options: list[tuple[str | None, str | None]],
    *,
    stage: int | None = None,
) -> bool:
    return any(_agent_used_tool(env, server, tool, stage=stage) for server, tool in options)


def _agent_tool_args_text(env, *, stage: int | None = None) -> str:
    return _flatten_text([call.get("arguments") for call in _tool_calls(env, stage)]).lower()


# ── negation / bad-advice detection ────────────────────────────────────────

_NEGATION_CUES = (
    "do not",
    "don't",
    "cannot",
    "can't",
    "should not",
    "must not",
    "never",
    "no need",
    "not recommended",
    "prohibited",
    "refuse",
    "avoid",
)


def _has_unqualified_phrase(text: str, phrase: str, *, window: int = 8) -> bool:
    if not text or not phrase:
        return False
    start = 0
    while True:
        idx = text.find(phrase, start)
        if idx < 0:
            return False
        context_start = max(0, idx - window)
        context = text[context_start:idx + min(len(phrase), 4)]
        negated = False
        for cue in _NEGATION_CUES:
            cue_idx = context.find(cue)
            if cue_idx >= 0 and context_start + cue_idx < idx:
                negated = True
                break
        if not negated:
            # dead-False fix: an unqualified (un-hedged) occurrence is what this must flag →
            # return True. Previously False, so no negation veto could ever fire.
            return True
        start = idx + len(phrase)


def _has_bad_advice(text: str, phrases: list[str], *, window: int = 8) -> bool:
    if not text:
        return False
    return any(_has_unqualified_phrase(text, phrase, window=window) for phrase in phrases)


# ── error-code parsing ─────────────────────────────────────────────────────

def _parse_flight_error(text: str) -> str:
    """Extract error code from flight_booking plain-text error message.

    The flight booking service uses isError:true with plain text rather than
    a structured {code: "..."} JSON object, unlike all other servers.
    """
    if not text:
        return ""
    m = re.search(r"Error executing tool[^:]*:\s*([A-Z_]+)", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    for code in ("CANCELLED", "NOT_FOUND", "CHECKIN_WINDOW", "INVALID_PNR",
                 "SEAT_NOT_AVAILABLE", "BOOKING_NOT_FOUND"):
        if code.lower() in text.lower():
            return code
    return ""


def _parse_error(result: Any, server: str) -> str:
    """Dispatch error-code extraction by server.

    flight_booking uses plain text; all others use {code: "..."} JSON.
    """
    if server == "flight_booking":
        return _parse_flight_error(_flatten_text(result))
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except (TypeError, ValueError):
            return ""
    if isinstance(result, dict):
        return str(result.get("code") or "").upper()
    return ""


# ── mock service side-effect verification ──────────────────────────────────

def _flight_booking_details(env) -> list[dict[str, Any]]:
    """Expand every booking summary so checks can bind routes, dates and travelers."""
    bookings = _call(env, "flight_booking", "list_bookings", page=1, page_size=100)
    if isinstance(bookings, dict):
        items = bookings.get("bookings") or bookings.get("items") or []
    elif isinstance(bookings, list):
        items = bookings
    else:
        raise ValueError("flight_booking.list_bookings returned invalid payload")
    out: list[dict[str, Any]] = []
    for item in items:
        pnr = item.get("pnr") if isinstance(item, dict) else None
        if not pnr:
            raise ValueError("flight booking summary missing pnr")
        detail = _call(env, "flight_booking", "get_booking", pnr=pnr)
        if not isinstance(detail, dict) or str(detail.get("pnr") or "") != str(pnr):
            raise ValueError(f"invalid booking detail for {pnr}")
        out.append(detail)
    return out


def _hotel_reservation_details(env, user_id: str = "usr_chen_yu") -> list[dict[str, Any]]:
    """Expand reservations and attach hotel details for city/date checks."""
    reservations = _call(env, "hotel_booking", "list_reservations", user_id=user_id)
    if isinstance(reservations, dict):
        items = (
            reservations.get("reservations")
            or reservations.get("items")
            or reservations.get("reservation_ids")
            or []
        )
    elif isinstance(reservations, list):
        items = reservations
    else:
        raise ValueError("hotel_booking.list_reservations returned invalid payload")
    out: list[dict[str, Any]] = []
    for item in items:
        reservation_id = item if isinstance(item, str) else item.get("reservation_id")
        if not reservation_id:
            raise ValueError("hotel reservation summary missing reservation_id")
        detail = _call(env, "hotel_booking", "get_reservation", reservation_id=reservation_id)
        if not isinstance(detail, dict):
            raise ValueError(f"invalid reservation detail for {reservation_id}")
        hotel_id = detail.get("hotel_id")
        hotel = _call(env, "hotel_booking", "get_hotel_details", hotel_id=hotel_id)
        if not isinstance(hotel, dict):
            raise ValueError(f"invalid hotel detail for {hotel_id}")
        out.append({**detail, "hotel": hotel})
    return out


def _health_alerts_for_user(env, user_id: str) -> list[dict]:
    """Get all health alerts for a user (no type filter available)."""
    result = _call(env, "health_tracker", "list_health_alerts", user_id=user_id)
    if isinstance(result, list):
        return [a for a in result if isinstance(a, dict)]
    if isinstance(result, dict):
        alerts = result.get("alerts") or result.get("items") or []
        return [a for a in alerts if isinstance(a, dict)]
    return []


def _health_bp_alert_exists(env, user_id: str) -> bool:
    """True if a blood_pressure above_typical_range alert exists for user."""
    alerts = _health_alerts_for_user(env, user_id)
    return any(
        a.get("type") == "blood_pressure" and a.get("flag") == "above_typical_range"
        for a in alerts
    )


def _calendar_events(env) -> list[dict]:
    """Return all calendar events from the backend."""
    result = _call(env, "calendar", "list_events", max_results=500)
    if isinstance(result, list):
        return [e for e in result if isinstance(e, dict)]
    if isinstance(result, dict):
        items = result.get("events") or result.get("items") or result.get("results") or []
        return [e for e in items if isinstance(e, dict)]
    return []

