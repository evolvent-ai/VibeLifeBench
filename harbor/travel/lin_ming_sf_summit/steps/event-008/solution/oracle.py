#!/usr/bin/env python3
"""Executable Harbor Oracle for Ming Lin's San Francisco summit trip."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "lin_ming_sf_summit"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The current San Francisco summit travel step was completed through the formal systems and recorded."

SERVICE_URLS = {
    "banking": "http://banking:8000/mcp",
    "calendar": "http://calendar:8000/mcp",
    "email": "http://email:8000/mcp",
    "flight_booking": "http://flight-booking:8000/mcp",
    "health_tracker": "http://health-tracker:8000/mcp",
    "hotel_booking": "http://hotel-booking:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "visa_and_advisory": "http://visa-and-advisory:8000/mcp",
}

USER_ID = "liming@company.com"
TRIP_ACCOUNT = "ACC_TRIP"
CALENDAR_ID = "CAL001"
NOTION_PAGE_ID = "PAGE_TRIP"


def _decode(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _unwrap_mcp(result: Any) -> Any:
    """Normalize the four supported MCP shapes, including empty-list reads."""
    if result is None:
        raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            return _decode(structured["result"])
        if structured not in (None, {}):
            return _decode(structured)
        result = blocks
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _decode(structured["result"])
    if structured not in (None, {}):
        return _decode(structured)
    content = result if isinstance(result, list) else getattr(result, "content", None)
    if content is not None:
        if content == []:
            return []
        for block in content:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict):
                text = block.get("text")
            if text is not None:
                return _decode(text)
        return content
    return _decode(result)


def _is_success(result: Any) -> bool:
    """Fail closed on error envelopes while accepting successful empty reads."""
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        return False
    try:
        value = _unwrap_mcp(result)
    except Exception:
        return False
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            return False
        if value.get("error") not in (None, False, ""):
            return False
        if str(value.get("status") or "").lower() in {"error", "failed", "failure"}:
            return False
        if value.get("ok") is False:
            return False
    if isinstance(value, list):
        return all(_is_success(item) for item in value) if value else True
    return value is not None


class Recorder:
    """Call MCP services and retain the exact per-turn ATIF audit trail."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(
        self,
        service: str,
        tool: str,
        arguments: dict[str, Any],
    ) -> Any:
        if service not in SERVICE_URLS:
            raise ValueError(f"unsupported MCP service: {service!r}")
        call_id = f"call-{len(self.calls) + 1}"
        recorded_arguments = dict(arguments)
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client

            configured = _decode(os.environ.get("HARBOR_MCP_URLS", "{}"))
            url = (configured.get(service) if isinstance(configured, dict) else None) or SERVICE_URLS[service]
            async with streamablehttp_client(url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw):
                raise RuntimeError(f"{service}.{tool} returned an error envelope: {value}")
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": recorded_arguments,
                "result": value,
                "success": True,
                "error": None,
            })
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": recorded_arguments,
                "result": {"error": error},
                "success": False,
                "error": error,
            })
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc

    def record_local(self, tool: str, arguments: dict[str, Any], result: Any) -> None:
        call_id = f"call-{len(self.calls) + 1}"
        self.calls.append({
            "tool_call_id": call_id,
            "function_name": f"workspace__{tool}",
            "arguments": dict(arguments),
            "result": result,
            "success": True,
            "error": None,
        })


def _empty_state() -> dict[str, Any]:
    return {"version": 1, "events": [], "vars": {}}


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return _empty_state()
    if not STATE_PATH.is_file() or STATE_PATH.is_symlink():
        raise RuntimeError(f"invalid Oracle state path: {STATE_PATH}")
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"oracle state is unreadable: {STATE_PATH}") from exc
    if not isinstance(value, dict) or value.get("version") != 1:
        raise RuntimeError("oracle state must be a versioned JSON object")
    if not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict):
        raise RuntimeError("oracle state has invalid events/vars fields")
    return value


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _save_state(state: dict[str, Any]) -> None:
    _atomic_write(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in keys:
            candidate = value.get(key)
            if isinstance(candidate, list):
                return [row for row in candidate if isinstance(row, dict)]
    return []


def _append(path_name: str, marker: str, text: str) -> None:
    if Path(path_name).name != path_name:
        raise ValueError("workspace path must be a file name")
    path = WORKSPACE / path_name
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    tag = f"<!-- oracle:{marker} -->"
    if tag in current:
        return
    heading = f"# {path.stem.replace('_', ' ').title()}\n" if not current else ""
    _atomic_write(path, heading + current.rstrip() + f"\n\n{tag}\n{text.rstrip()}\n")


def _rich(text: str) -> dict[str, Any]:
    return {
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


async def _read_workspace_file(recorder: Recorder, name: str) -> str:
    path = WORKSPACE / name
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required workspace file is unavailable: {path}")
    text = path.read_text(encoding="utf-8")
    recorder.record_local("read_file", {"path": str(path), "filename": name}, {"characters": len(text)})
    return text


async def _search_outbound(
    recorder: Recorder,
    *,
    departure_date: str,
    cabin: str = "BUSINESS",
    non_stop: bool = False,
) -> list[dict[str, Any]]:
    arguments = {
        "origin": "PEK",
        "destination": "SFO",
        "departure_date": departure_date,
        "adults": 1,
        "cabin": cabin,
        "currency": "CNY",
        "max_results": 50,
        "sort": "price_asc",
        "non_stop": non_stop,
    }
    result = await recorder.call("flight_booking", "search_flights", arguments)
    return _rows(result, "items", "offers", "results")


async def _search_hotels(recorder: Recorder) -> list[dict[str, Any]]:
    arguments = {
        "city_or_geo": "San Francisco",
        "check_in": "2026-03-27",
        "check_out": "2026-03-31",
        "guests": 1,
        "filters": {"sort": "price_asc", "limit": 50},
        "page": 1,
    }
    result = await recorder.call("hotel_booking", "search_hotels", arguments)
    return _rows(result, "items", "hotels", "results")


async def _flight_details(recorder: Recorder) -> list[dict[str, Any]]:
    listing = await recorder.call(
        "flight_booking", "list_bookings", {"email": USER_ID, "page": 1, "page_size": 100}
    )
    details: list[dict[str, Any]] = []
    for row in _rows(listing, "bookings", "items", "results"):
        pnr = row.get("pnr")
        if pnr:
            detail = await recorder.call("flight_booking", "get_booking", {"pnr": str(pnr)})
            if isinstance(detail, dict):
                details.append(detail)
    return details


async def _book_offer(recorder: Recorder, offer: dict[str, Any]) -> dict[str, Any]:
    offer_id = str(offer.get("offer_id") or "")
    if not offer_id:
        raise RuntimeError("selected flight offer has no offer_id")
    await recorder.call("flight_booking", "get_flight_offer", {"offer_id": offer_id})
    await recorder.call("flight_booking", "price_offer", {"offer_id": offer_id})
    booked = await recorder.call("flight_booking", "create_booking", {
        "offer_id": offer_id,
        "passengers": [{
            "type": "ADT",
            "given_name": "Ming",
            "family_name": "Lin",
            "passport_no": "E12345678",
            "nationality": "CN",
        }],
        "contact": {"email": USER_ID, "phone": "+8613800000000"},
        "payment": {"method": "CARD", "card_last4": "4242"},
        "hold": False,
    })
    if not isinstance(booked, dict) or not booked.get("pnr"):
        raise RuntimeError("flight booking did not return a PNR")
    return booked


async def _ensure_direct_outbound(recorder: Recorder, state: dict[str, Any]) -> None:
    details = await _flight_details(recorder)
    for booking in details:
        segments = booking.get("segments") or []
        if len(segments) == 1 and str(segments[0].get("origin")) == "PEK" and str(segments[0].get("dest")) == "SFO":
            state["vars"]["direct_outbound_pnr"] = str(booking.get("pnr") or "")
            return
    offers = await _search_outbound(recorder, departure_date="2026-03-26", cabin="BUSINESS", non_stop=True)
    if not offers:
        offers = await _search_outbound(recorder, departure_date="2026-03-27", cabin="BUSINESS", non_stop=True)
    if not offers:
        raise RuntimeError("no released direct business-class outbound offer")
    booked = await _book_offer(recorder, offers[0])
    state["vars"]["direct_outbound_pnr"] = str(booked["pnr"])


async def _ensure_hkg_outbound(recorder: Recorder, state: dict[str, Any]) -> None:
    details = await _flight_details(recorder)
    for booking in details:
        segments = booking.get("segments") or []
        if (
            str(booking.get("status", "")).upper() in {"TICKETED", "HOLD", "CHANGED"}
            and len(segments) >= 2
            and str(segments[0].get("origin", "")).upper() == "PEK"
            and str(segments[0].get("dest", segments[0].get("destination", ""))).upper() == "HKG"
            and str(segments[1].get("origin", "")).upper() == "HKG"
            and str(segments[1].get("dest", segments[1].get("destination", ""))).upper() == "SFO"
            and str(segments[0].get("depart_dt", ""))[:10] in {"2026-03-26", "2026-03-27"}
        ):
            state["vars"]["hkg_outbound_pnr"] = str(booking.get("pnr") or "")
            return
    offers = await _search_outbound(recorder, departure_date="2026-03-26", cabin="BUSINESS")
    if not offers:
        offers = await _search_outbound(recorder, departure_date="2026-03-27", cabin="BUSINESS")
    offer = None
    for candidate in offers:
        offer_id = str(candidate.get("offer_id") or "")
        if not offer_id:
            continue
        detail = await recorder.call(
            "flight_booking", "get_flight_offer", {"offer_id": offer_id}
        )
        segments = detail.get("segments") if isinstance(detail, dict) else []
        if any(
            str(segment.get("origin", "")).upper() == "HKG"
            or str(segment.get("destination", "")).upper() == "HKG"
            for segment in segments or []
            if isinstance(segment, dict)
        ):
            offer = candidate
            break
    if offer is None:
        raise RuntimeError("no released Hong Kong connecting offer")
    booked = await _book_offer(recorder, offer)
    state["vars"]["hkg_outbound_pnr"] = str(booked["pnr"])


async def _ensure_return(recorder: Recorder, state: dict[str, Any]) -> None:
    details = await _flight_details(recorder)
    for booking in details:
        segments = booking.get("segments") or []
        if any(str(segment.get("origin")) == "SFO" and str(segment.get("dest")) == "PEK" for segment in segments):
            state["vars"]["return_pnr"] = str(booking.get("pnr") or "")
            return
    result = await recorder.call("flight_booking", "search_flights", {
        "origin": "SFO",
        "destination": "PEK",
        "departure_date": "2026-04-05",
        "adults": 1,
        "cabin": "BUSINESS",
        "currency": "CNY",
        "max_results": 50,
        "sort": "price_asc",
        "non_stop": True,
    })
    offers = _rows(result, "items", "offers", "results")
    if not offers:
        raise RuntimeError("no released return business-class offer")
    booked = await _book_offer(recorder, offers[0])
    state["vars"]["return_pnr"] = str(booked["pnr"])


async def _hotel_details(recorder: Recorder) -> list[dict[str, Any]]:
    listing = await recorder.call("hotel_booking", "list_reservations", {"user_id": USER_ID})
    details: list[dict[str, Any]] = []
    ids = listing.get("reservation_ids") if isinstance(listing, dict) else []
    for reservation_id in ids or []:
        detail = await recorder.call(
            "hotel_booking", "get_reservation", {"reservation_id": str(reservation_id)}
        )
        if isinstance(detail, dict):
            details.append(detail)
    return details


async def _ensure_hotel(recorder: Recorder, state: dict[str, Any]) -> None:
    details = await _hotel_details(recorder)
    for reservation in details:
        if str(reservation.get("check_in", "")) <= "2026-03-28" and str(reservation.get("check_out", "")) >= "2026-03-30":
            state["vars"]["hotel_reservation_id"] = str(reservation.get("reservation_id") or "")
            return
    hotels = await _search_hotels(recorder)
    if not hotels:
        raise RuntimeError("no released San Francisco hotel option")
    hotel_id = str(hotels[0].get("hotel_id") or "")
    if not hotel_id:
        raise RuntimeError("selected hotel has no hotel_id")
    await recorder.call("hotel_booking", "get_hotel_details", {"hotel_id": hotel_id})
    availability = await recorder.call("hotel_booking", "get_room_availability", {
        "hotel_id": hotel_id,
        "check_in": "2026-03-27",
        "check_out": "2026-03-31",
        "guests": 1,
    })
    plans = _rows(availability, "rate_plans", "items", "results")
    if not plans:
        raise RuntimeError("selected hotel has no released room inventory")
    reservation = await recorder.call("hotel_booking", "create_reservation", {
        "rate_plan_id": str(plans[0]["rate_plan_id"]),
        "guest_profile": {
            "first_name": "Ming",
            "last_name": "Lin",
            "email": USER_ID,
            "phone": "+8613800000000",
            "user_id": USER_ID,
        },
        "payment_method_id": "pm_corporate_travel",
        "special_requests": "Quiet room suitable for a business traveler.",
    })
    if not isinstance(reservation, dict) or not reservation.get("reservation_id"):
        raise RuntimeError("hotel reservation did not return an id")
    state["vars"]["hotel_reservation_id"] = str(reservation["reservation_id"])


async def _append_notion(recorder: Recorder, marker: str, text: str) -> None:
    existing = await recorder.call(
        "notion", "API-get-block-children", {"block_id": NOTION_PAGE_ID, "page_size": 10000}
    )
    if marker.lower() in json.dumps(existing, ensure_ascii=False).lower():
        text = f"{marker}: reviewed; {text}"
    else:
        text = f"{marker}: {text}"
    await recorder.call("notion", "API-patch-block-children", {
        "block_id": NOTION_PAGE_ID,
        "children": [_rich(text)],
    })


async def _ensure_client_visit(recorder: Recorder, state: dict[str, Any]) -> None:
    events = await recorder.call("calendar", "list_events", {
        "time_min": "2026-03-27T00:00:00-07:00",
        "time_max": "2026-03-31T23:59:59-07:00",
        "calendar_id": CALENDAR_ID,
        "max_results": 100,
    })
    for event in _rows(events, "items", "events", "results"):
        if "client visit" in json.dumps(event, ensure_ascii=False).lower():
            state["vars"]["client_visit_event_id"] = str(event.get("event_id") or event.get("id") or "")
            return
    created = await recorder.call("calendar", "create_event", {
        "summary": "San Francisco client visit",
        "start": "2026-03-29T14:00:00-07:00",
        "end": "2026-03-29T16:00:00-07:00",
        "description": "Downtown client visit; keep the internal stand-up visible when reviewing the day.",
        "location": "Downtown San Francisco",
        "calendar_id": CALENDAR_ID,
        "attendees": [{"email": USER_ID, "name": "Ming Lin", "response_status": "accepted"}],
        "reminders": [{"method": "popup", "minutes_before": 30}],
    })
    if isinstance(created, dict):
        state["vars"]["client_visit_event_id"] = str(created.get("event_id") or created.get("id") or "")


async def _ensure_evus(recorder: Recorder, state: dict[str, Any]) -> None:
    applications = await recorder.call(
        "visa_and_advisory", "list_visa_applications", {"user_id": USER_ID}
    )
    app_id = ""
    detail: dict[str, Any] = {}
    for row in _rows(applications, "applications", "items", "results"):
        candidate = str(row.get("application_id") or "")
        if not candidate:
            continue
        current = await recorder.call(
            "visa_and_advisory", "get_visa_application", {"application_id": candidate}
        )
        if isinstance(current, dict) and "evus" in json.dumps(current, ensure_ascii=False).lower():
            app_id, detail = candidate, current
            break
    if not app_id:
        raise RuntimeError("the released EVUS renewal draft is not discoverable")
    state["vars"]["evus_application_id"] = app_id
    if str(detail.get("status") or "").lower() in {"processing", "approved", "active", "issued", "granted"}:
        return
    uploaded = await recorder.call("visa_and_advisory", "upload_document", {
        "application_id": app_id,
        "kind": "passport",
        "doc_ref": "EVUS-renewal-passport-E12345678",
    })
    doc_id = str(uploaded.get("doc_id") or "") if isinstance(uploaded, dict) else ""
    await recorder.call("visa_and_advisory", "submit_visa_application", {
        "application_id": app_id,
        "answers": {
            "passport_number": "E12345678",
            "passport_expiry": "2026-05-30",
            "purpose": "business",
            "kind": "EVUS_renewal",
            "prior_enrollment_number": "EN1234567890",
            "prior_expiry": "2026-03-25",
        },
        "docs_refs": [doc_id] if doc_id else [],
        "payment_method_id": "pm_corporate_travel",
    })


async def _ensure_approval_email(recorder: Recorder, state: dict[str, Any]) -> None:
    sent = await recorder.call("email", "get_emails", {"folder": "Sent", "page": 1, "page_size": 100})
    for row in _rows(sent, "emails", "messages", "items"):
        if "san francisco summit travel pre-clearance" in str(row.get("subject") or "").lower():
            state["vars"]["approval_email_id"] = str(row.get("email_id") or row.get("id") or "")
            return
    result = await recorder.call("email", "send_email", {
        "to": "zhang_manager@company.com",
        "subject": "Approval request: San Francisco summit travel pre-clearance",
        "body": (
            "Manager Zhang, please provide written approval for Ming Lin's San Francisco industry summit trip. "
            "The current pre-clearance amount is CNY 14,820, including flight, hotel, local transport, and EVUS-related costs. "
            "This exceeds the CNY 5,000 written-approval threshold but remains within the CNY 15,000 trip cap. "
            "The itinerary and expense breakdown are archived in the Notion trip page."
        ),
    })
    if isinstance(result, dict):
        state["vars"]["approval_email_id"] = str(result.get("email_id") or result.get("id") or "")


async def _select_changed_segment_seat(recorder: Recorder, state: dict[str, Any]) -> None:
    details = await _flight_details(recorder)
    target: tuple[str, int] | None = None
    for booking in details:
        pnr = str(booking.get("pnr") or "")
        for index, segment in enumerate(booking.get("segments") or []):
            if str(segment.get("flight_no") or "").upper() == "CX870":
                target = (pnr, index)
                break
        if target:
            break
    if target is None:
        for booking in details:
            pnr = str(booking.get("pnr") or "")
            for index, segment in enumerate(booking.get("segments") or []):
                if str(segment.get("origin")) == "HKG" and str(segment.get("dest")) == "SFO":
                    target = (pnr, index)
                    break
            if target:
                break
    if target is None or not target[0]:
        raise RuntimeError("no confirmed HKG-SFO booking segment is available")
    pnr, segment_idx = target
    await recorder.call("flight_booking", "get_seat_map", {"pnr": pnr, "segment_idx": segment_idx})
    result = await recorder.call("flight_booking", "check_in", {
        "pnr": pnr,
        "segment_idx": segment_idx,
        "pax_indices": [0],
    })
    state["vars"]["seat_booking_pnr"] = pnr
    if isinstance(result, dict):
        assigned = result.get("checked_in") or []
        if assigned and isinstance(assigned[0], dict):
            state["vars"]["assigned_seat"] = str(assigned[0].get("seat") or "")


async def _handle_record_event(
    recorder: Recorder,
    state: dict[str, Any],
    spec: dict[str, Any],
    action: dict[str, Any],
) -> None:
    source_event_id = str(action.get("source_event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")

    if source_event_id == "u0":
        await _read_workspace_file(recorder, "USER.md")
        await _read_workspace_file(recorder, "TOOLS.md")
        offers = await _search_outbound(recorder, departure_date="2026-03-26")
        if offers:
            await recorder.call("flight_booking", "get_flight_offer", {"offer_id": str(offers[0]["offer_id"])})
        await _search_hotels(recorder)
        await recorder.call("health_tracker", "get_goals", {"user_id": USER_ID, "status": "active"})
        await recorder.call("health_tracker", "list_health_alerts", {"user_id": USER_ID, "limit": 50})
        await recorder.call("visa_and_advisory", "check_entry_requirements", {
            "nationality": "CN", "destination": "US", "purpose": "business", "transit_countries": ["HK"]
        })
        await recorder.call("visa_and_advisory", "list_visa_applications", {"user_id": USER_ID})
        await recorder.call("banking", "get_account", {"account_id": TRIP_ACCOUNT})
        _append("trip_plan.md", "scope", "Ming Lin's San Francisco industry summit runs March 28-30. The working scope covers flight and hotel research, passport and EVUS readiness, calendar management, and reimbursement pre-clearance. The health constraint is a maximum of ten hours for any single economy-class segment, so business class or a suitable connecting itinerary is required for longer travel.")
    elif source_event_id == "n1":
        await recorder.call("visa_and_advisory", "check_entry_requirements", {
            "nationality": "CN", "destination": "US", "purpose": "business", "transit_countries": ["HK"]
        })
        await recorder.call("visa_and_advisory", "list_visa_applications", {"user_id": USER_ID})
        _append("trip_plan.md", "passport", "Passport expiry is 2026-05-30 and the planned return is 2026-04-05, leaving a short margin. Obtain written confirmation from the operating airline or carrier and verify official CBP guidance. The contingency is to renew or replace the passport, keep bookings refundable or hold the booking, and escalate before departure if confirmation is not obtained.")
        _append("decision_log.md", "passport", "Passport and EVUS remain separate entry controls. Official CBP and operating-airline confirmation is required because the expiry margin after the 2026-04-05 return is limited.")
    elif source_event_id == "u2":
        await _search_outbound(recorder, departure_date="2026-03-26")
        await _search_hotels(recorder)
        await recorder.call("health_tracker", "list_health_alerts", {"user_id": USER_ID, "limit": 50})
        await recorder.call("health_tracker", "get_goals", {"user_id": USER_ID, "status": "active"})
    elif source_event_id == "n3":
        await recorder.call("banking", "get_account", {"account_id": TRIP_ACCOUNT})
        await recorder.call("banking", "list_transactions", {"account_id": TRIP_ACCOUNT, "limit": 100})
        _append("budget_tracker.md", "policy", "Travel budget cap: CNY 15000. Any expense above CNY 5000 requires Manager Zhang's prior written approval. Working lines: flight, hotel, local transport, entry documentation, and total.")
    elif source_event_id == "w4":
        await recorder.call("banking", "list_transactions", {"account_id": TRIP_ACCOUNT, "limit": 100})
        _append("budget_tracker.md", "fx-742", "Internal pre-clearance exchange rate: 1 USD = 7.42 CNY. Example conversion: USD 1,000 x 7.42 = CNY 7,420. This is a budget conversion basis, not the final reimbursement settlement rate.")
    elif source_event_id == "u5":
        await _ensure_direct_outbound(recorder, state)
        _append("budget_tracker.md", "outbound", "Flight booking recorded in the corporate travel platform. It is business class for the long direct segment and remains subject to the written approval workflow.")
    elif source_event_id in {"n7", "w7b"}:
        await _search_outbound(recorder, departure_date="2026-03-26")
        _append("decision_log.md", "direct-cancelled", "The watched direct PEK-SFO services were cancelled. Search live totals for a connecting itinerary through Hong Kong; compare the recalculated fuel surcharge rather than assuming every airline increased prices.")
    elif source_event_id == "u8":
        await _ensure_hkg_outbound(recorder, state)
        _append("trip_plan.md", "hkg-itinerary", "A confirmed PEK-HKG-SFO connecting itinerary is retained as the outbound alternative after the direct-flight cancellation. Hong Kong connection timing and operational updates remain on watch.")
    elif source_event_id == "w9":
        details = await _flight_details(recorder)
        if details:
            await recorder.call("flight_booking", "get_booking", {"pnr": str(details[-1].get("pnr") or details[0].get("pnr"))})
        _append("trip_plan.md", "hkg-weather", "Thunderstorms may affect the Hong Kong transit window. Keep a connection buffer, monitor updates and delays, and retain an alternative or rebook contingency if the connecting flight is disrupted.")
        _append("decision_log.md", "hkg-weather", "Weather advisory reviewed for the HKG connection; monitor formal flight updates and preserve a rebooking alternative.")
    elif source_event_id == "n10":
        await _ensure_evus(recorder, state)
        _append("trip_plan.md", "evus", "The EVUS renewal draft tied to prior enrollment EN1234567890 was submitted through the formal visa system before the existing enrollment's 2026-03-25 expiry.")
    elif source_event_id == "u11":
        await recorder.call("visa_and_advisory", "check_entry_requirements", {
            "nationality": "CN", "destination": "US", "purpose": "business", "transit_countries": ["HK"]
        })
        _append("decision_log.md", "entry-remedy", "Do not defer passport or EVUS readiness until arrival. Preserve the official confirmation and passport-renewal contingency while the submitted EVUS renewal is tracked.")
    elif source_event_id in {"n13", "w13b"}:
        await _search_hotels(recorder)
        await recorder.call("banking", "get_account", {"account_id": TRIP_ACCOUNT})
        _append("budget_tracker.md", "hotel-surge", "San Francisco hotel price surge reviewed against live alternatives before booking. The updated internal pre-clearance exchange rate is 1 USD = 7.58 CNY; internal pre-clearance and final reimbursement exchange rates may differ. Reassess value and control the budget before confirming the hotel.")
    elif source_event_id == "n14":
        await _flight_details(recorder)
        await _hotel_details(recorder)
        await recorder.call("calendar", "list_events", {
            "time_min": "2026-03-15T00:00:00+08:00", "time_max": "2026-04-10T23:59:59+08:00", "calendar_id": CALENDAR_ID, "max_results": 100
        })
        await _ensure_return(recorder, state)
    elif source_event_id == "u15":
        await _ensure_hotel(recorder, state)
        _append("budget_tracker.md", "hotel-booked", "Hotel: confirmed San Francisco stay for 2026-03-27 through 2026-03-31, covering the summit window. Flight and hotel remain in the expense breakdown.")
    elif source_event_id == "n17":
        await recorder.call("calendar", "list_events", {
            "time_min": "2026-03-28T00:00:00-07:00", "time_max": "2026-03-30T23:59:59-07:00", "calendar_id": CALENDAR_ID, "max_results": 100
        })
        _append("trip_plan.md", "meeting-conflict", "The March 29 client visit and internal stand-up are both visible. Their schedule does not directly overlap, but the day has a travel and meeting conflict that requires a buffer between the stand-up and client visit.")
        _append("decision_log.md", "meeting-conflict", "Calendar conflict review covers both the client visit and internal stand-up; preserve transfer time and avoid an overlap.")
    elif source_event_id == "u18":
        await _ensure_client_visit(recorder, state)
        _append("trip_plan.md", "meetings", "Calendar itinerary updated: internal stand-up on March 29 from 09:00-10:00 and San Francisco client visit from 14:00-16:00 in Downtown San Francisco.")
    elif source_event_id == "w19":
        details = await _flight_details(recorder)
        return_segment: dict[str, Any] | None = None
        for booking in details:
            for segment in booking.get("segments") or []:
                if str(segment.get("origin")) == "SFO":
                    return_segment = segment
                    break
        if return_segment:
            await recorder.call("flight_booking", "get_flight_status", {
                "flight_no": str(return_segment["flight_no"]),
                "date": str(return_segment["depart_dt"])[:10],
            })
        _append("trip_plan.md", "sfo-wind", "A San Francisco high-wind advisory may delay flight arrivals or departures. Monitor the return flight and airport updates, arrive early, preserve a schedule buffer, and keep a change-flight or rebook contingency.")
        _append("decision_log.md", "sfo-wind", "Return-flight wind risk reviewed with an early-arrival buffer and alternative rebooking plan.")
    elif source_event_id == "n21":
        await recorder.call("banking", "get_account", {"account_id": TRIP_ACCOUNT})
        await recorder.call("banking", "list_transactions", {"account_id": TRIP_ACCOUNT, "limit": 500})
        await _append_notion(recorder, "REIMBURSEMENT_POLICY_V1", "Trip flight and hotel records, expense breakdown, budget, approval evidence, receipts, and reimbursement exchange-rate basis reviewed under the latest travel policy.")
    elif source_event_id == "u22":
        await _append_notion(recorder, "PRE_CLEARANCE_V1", "San Francisco summit itinerary: confirmed flight bookings and hotel stay. Expense and reimbursement pre-clearance total is CNY 14,820; written approval is required because the request exceeds CNY 5,000.")
        await _ensure_approval_email(recorder, state)
        _append("budget_tracker.md", "preclearance-total", "Expense breakdown: flight, hotel, local transport, and EVUS-related costs. Pre-clearance total: CNY 14,820. Written approval requested from Manager Zhang; reimbursement archive pending receipts and final Finance settlement.")
    elif source_event_id == "n24":
        await _select_changed_segment_seat(recorder, state)
        _append("trip_plan.md", "aircraft-change", "The HKG-SFO aircraft change was verified in the confirmed booking. The prior seat status was reviewed and a valid seat was assigned on the changed aircraft.")
    elif source_event_id == "u25":
        await _flight_details(recorder)
        await _hotel_details(recorder)
        await recorder.call("calendar", "list_events", {
            "time_min": "2026-03-15T00:00:00+08:00", "time_max": "2026-04-10T23:59:59+08:00", "calendar_id": CALENDAR_ID, "max_results": 100
        })
        await recorder.call("banking", "list_transactions", {"account_id": TRIP_ACCOUNT, "limit": 500})
    else:
        raise ValueError(f"unsupported source event: {source_event_id!r}")

    state["events"] = [row for row in state["events"] if row.get("source_event_id") != source_event_id]
    state["events"].append({"source_event_id": source_event_id, "virtual_stage": int(spec["virtual_stage"])})


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = (
        "step", "virtual_stage", "source_event_id", "response", "response_paraphrase",
        "actions", "expected_env", "expected_checks", "expected_stage_weight",
    )
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    if not isinstance(spec["source_event_id"], str) or not spec["source_event_id"]:
        raise ValueError("source_event_id must be non-empty")
    if not isinstance(spec["actions"], list) or not spec["actions"]:
        raise ValueError("actions must be a non-empty list")
    if not isinstance(spec["expected_env"], dict):
        raise ValueError("expected_env must be an object")
    for key in ("preceding_releases", "released_mutations"):
        if not isinstance(spec["expected_env"].get(key), list):
            raise ValueError(f"expected_env.{key} must be a list")
    for env_name, expected in (
        ("HARBOR_STEP_NAME", spec["step"]),
        ("SOURCE_EVENT_ID", spec["source_event_id"]),
        ("VIRTUAL_STAGE", str(spec["virtual_stage"])),
    ):
        actual = os.environ.get(env_name)
        if actual and actual != expected:
            raise RuntimeError(f"{env_name}={actual!r} does not match {expected!r}")


def _response(spec: dict[str, Any]) -> str:
    style = os.environ.get("ORACLE_STYLE", "canonical").strip().lower()
    if style not in {"canonical", "paraphrase"}:
        raise ValueError(f"unsupported ORACLE_STYLE: {style!r}")
    value = spec.get("response_paraphrase" if style == "paraphrase" else "response")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("response text is missing")
    return value


def _write_trajectory(spec: dict[str, Any], recorder: Recorder, response: str) -> None:
    trajectory = {
        "schema_version": "ATIF-v1.7",
        "session_id": f"oracle-{spec['step']}",
        "agent": {"name": f"{TASK_ID}-oracle", "version": "1.0.0"},
        "steps": [
            {"step_id": 1, "source": "user", "message": str(spec["source_event_id"])},
            {
                "step_id": 2,
                "source": "agent",
                "message": response,
                "tool_calls": [
                    {
                        "tool_call_id": row["tool_call_id"],
                        "function_name": row["function_name"],
                        "arguments": row["arguments"],
                    }
                    for row in recorder.calls
                ],
                "observation": {
                    "results": [
                        {
                            "source_call_id": row["tool_call_id"],
                            "content": json.dumps(row["result"], ensure_ascii=False, default=str),
                            "extra": {"success": row["success"], "error": row["error"]},
                        }
                        for row in recorder.calls
                    ]
                },
                "llm_call_count": 0,
            },
        ],
        "final_metrics": {
            "tool_calls": len(recorder.calls),
            "tool_errors": sum(not row["success"] for row in recorder.calls),
        },
    }
    _atomic_write(LOGS / "trajectory.json", json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n")


async def _run(spec: dict[str, Any]) -> str:
    _validate_spec(spec)
    response = _response(spec)
    state = _load_state()
    recorder = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = str(action.get("kind") or "")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(
                f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. "
                f"Known kinds: {known}."
            )
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    _save_state(state)
    _write_trajectory(spec, recorder, response)
    return response


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: oracle.py STEP_SPEC", file=sys.stderr)
        return 1
    try:
        spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(asyncio.run(_run(spec)))
        return 0
    except Exception as exc:
        print(f"oracle.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
