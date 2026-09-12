#!/usr/bin/env python3
"""Executable Harbor Oracle for Li Wei's accessible Kansai family trip."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "family_medical_accessible_japan_53d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The Kansai family-trip records were updated through the authorized systems and the current evidence was preserved."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "credit_card": "http://credit-card:8000/mcp",
    "email": "http://email:8000/mcp",
    "flight_booking": "http://flight-booking:8000/mcp",
    "hotel_booking": "http://hotel-booking:8000/mcp",
    "maps": "http://maps:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "rail_booking": "http://rail-booking:8000/mcp",
    "visa_and_advisory": "http://visa-and-advisory:8000/mcp",
    "weather": "http://weather:8000/mcp",
}

USER_ID = "trav_liwei"
USER_EMAIL = "liwei@example.com"
NOTION_PROFILE = "pg_access_notes"
NOTION_RETROSPECTIVE = "pg_past_trip_lessons"
OLD_OFFER = "of_kansai_daytime_refundable_hold"
NEW_OFFER = "of_kansai_price_drop_20261008"
HOTEL_KYOTO = "jp_ht_001"
HOTEL_OSAKA = "jp_ht_006"
INSURANCE_MID = "<insurance-options-20260916@kansai-cover.example>"
HOTEL_REQUEST_MID = "<access-request-kyoto-6142@higashiyama-garden.example>"
CONFIRM_MID = "<kansai-confirm-20261011@kansai-travel.example>"


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
    """Normalize supported MCP result shapes, including successful empty reads."""
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

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        if service not in SERVICE_URLS:
            raise ValueError(f"unsupported MCP service: {service!r}")
        call_id = f"call-{len(self.calls) + 1}"
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
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": dict(arguments), "result": value, "success": True, "error": None})
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": dict(arguments), "result": {"error": error}, "success": False, "error": error})
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc


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


def _append(name: str, marker: str, text: str) -> None:
    if Path(name).name != name:
        raise ValueError("workspace path must be a file name")
    path = WORKSPACE / name
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    tag = f"<!-- oracle:{marker} -->"
    if tag in current:
        return
    heading = f"# {path.stem.replace('_', ' ').title()}\n" if not current else ""
    _atomic_write(path, heading + current.rstrip() + f"\n\n{tag}\n{text.rstrip()}\n")


def _rich(text: str) -> dict[str, Any]:
    return {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


async def _notion_append(recorder: Recorder, text: str, page_id: str = NOTION_PROFILE) -> None:
    await recorder.call("notion", "API-get-block-children", {"block_id": page_id, "page_size": 10000})
    await recorder.call("notion", "API-patch-block-children", {"block_id": page_id, "children": [_rich(text)]})


async def _find_and_read_email(recorder: Recorder, query: str, message_id: str) -> dict[str, Any]:
    result = await recorder.call("email", "search_emails", {"query": query, "folder": "INBOX", "page": 1, "page_size": 20})
    rows = _rows(result, "emails", "results")
    row = next((x for x in rows if x.get("message_id") == message_id), None)
    if not row or not row.get("email_id"):
        raise RuntimeError(f"expected email thread was not found: {message_id}")
    detail = await recorder.call("email", "read_email", {"email_id": str(row["email_id"])})
    return detail if isinstance(detail, dict) else {}


async def _handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    source_event_id = str(action.get("source_event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"])

    if stage == 0:
        _append("trip_plan.md", "initial", "Kansai family trip candidate: Osaka, Kyoto, Nara, and Arima Onsen, with Osaka entry and return from 2026-10-12 through 2026-10-19. Keep the itinerary gentle and reversible; each option remains unpaid and requires evidence before authorization.")
        _append("budget_ledger.md", "initial", "Planning estimate and status: budget cap is CNY 42000; every amount is an estimate until supported by a receipt or vendor record. Payment status is unpaid and evidence is pending.")
        _append("risk_register.md", "initial", "Mobility accessibility is the primary logistics risk. Owner: Li Wei. Next review: 2026-09-02. Check step-free routes, elevator access, walking distance, and weather before confirmation.")
        _append("decision_log.md", "initial", "Decision: keep Osaka, Kyoto, Nara, and Arima Onsen as candidate options. Payment remains unpaid and authorization is not yet granted. Next action: research reversible transport and lodging evidence.")
    elif stage == 1:
        await recorder.call("notion", "API-post-search", {"query": "family mobility household profile", "filter": {"value": "page"}, "page_size": 100})
        await recorder.call("notion", "API-get-block-children", {"block_id": NOTION_PROFILE, "page_size": 10000})
        await _notion_append(recorder, "Family profile read and persisted for travel logistics: father Li Wei's father avoids red-eye flights, very early departures, and long standing; mother prefers mobility accessibility, step-free routes, an elevator or room near the elevator, and a short station walk. Passport data is handled as private data and only masked references are retained. This is logistics information, not a medical clearance.")
        _append("risk_register.md", "profile", "Profile evidence: father avoids red-eye and very early departures; mother has slower walking and needs mobility accessibility, step-free routes, and a room near the elevator. Passport and identity-document details stay private data; retain only masked references. Owner: Li Wei. Next review: 2026-09-03.")
    elif stage == 2:
        _append("trip_plan.md", "dates", "Working dates are 2026-10-12 to 2026-10-19, with a one-day flexibility window if a materially better option appears. Osaka, Kyoto, Nara, and Arima Onsen remain candidate stops.")
        _append("budget_ledger.md", "cap", "Budget cap: CNY 42000. Planning status is tentative; payment remains unpaid pending explicit authorization and refundable terms. Evidence time: 2026-09-03.")
    elif stage == 3:
        await recorder.call("flight_booking", "search_flights", {"origin": "PVG", "destination": "KIX", "departure_date": "2026-10-12", "adults": 3, "cabin": "ECONOMY", "currency": "CNY", "max_results": 20, "sort": "price_asc", "non_stop": True})
        _append("trip_plan.md", "flight-inventory", "Flight evidence: MU737 runs PVG to KIX on 2026-10-12 at 10:00, a daytime nonstop flight for three travelers. The fare bucket supports a hold and has refundable and changeable rules; no ticket is authorized yet.")
        _append("decision_log.md", "flight-inventory", "Candidate MU737 PVG-KIX 2026-10-12 10:00 is daytime, direct, and refundable. Hold is preferred over payment while authorization remains pending. Owner: Li Wei. Next action: compare accessible lodging.")
    elif stage == 4:
        await recorder.call("hotel_booking", "search_hotels", {"city_or_geo": "Kyoto", "check_in": "2026-10-15", "check_out": "2026-10-16", "guests": 2, "filters": {"amenities": ["accessible_room", "elevator"], "refundable_only": True, "limit": 50}, "page": 1})
        await recorder.call("hotel_booking", "get_hotel_details", {"hotel_id": HOTEL_KYOTO})
        availability = await recorder.call("hotel_booking", "get_room_availability", {"hotel_id": HOTEL_KYOTO, "check_in": "2026-10-15", "check_out": "2026-10-16", "guests": 2})
        plans = _rows(availability, "items", "rate_plans", "results")
        candidate = next((row for row in plans if row.get("flavor") == "flex" and row.get("refundable") is True), None)
        if not isinstance(candidate, dict) or not candidate.get("nightly_prices") or not candidate.get("currency"):
            raise RuntimeError("Kyoto refundable room evidence was not found")
        nightly = candidate["nightly_prices"][0]
        inventory = candidate.get("inventory_remaining")
        currency = str(candidate["currency"])
        _append("trip_plan.md", "kyoto-hotel", f"Kyoto accessible-room evidence: {HOTEL_KYOTO} has elevator and step-free access. The 2026-10-15 flex room is {currency} {nightly} nightly with inventory {inventory} and free cancellation, so it is a scarce refundable option.")
        _append("decision_log.md", "kyoto-hotel", f"Keep {HOTEL_KYOTO} as the Kyoto candidate because it offers an accessible room, elevator access, and free cancellation. Inventory {inventory} and price {currency} {nightly} require a prompt but reversible decision.")
    elif stage == 5:
        _append("trip_plan.md", "preferences", "Mobility plan: father avoids red-eye and very early flights; mother needs an accessible, step-free route, an elevator or room near the elevator, and a short station walk. Arima Onsen may be one night only; avoid a staircase-heavy inn and pre-plan every transfer.")
        _append("decision_log.md", "preferences", "Family preference record: father needs a daytime schedule rather than red-eye or very early departure; mother needs accessible lodging, elevator access, step-free movement, and station walking support. Next action: sequence transfers with buffers.")
    elif stage == 6:
        await recorder.call("weather", "get_forecast_daily", {"geo": "osaka", "days": 1})
        await recorder.call("flight_booking", "search_flights", {"origin": "PVG", "destination": "KIX", "departure_date": "2026-10-12", "adults": 3, "cabin": "ECONOMY", "max_results": 20})
        await recorder.call("hotel_booking", "search_hotels", {"city_or_geo": "Osaka", "check_in": "2026-10-12", "check_out": "2026-10-13", "guests": 3, "filters": {"limit": 20}, "page": 1})
        await recorder.call("visa_and_advisory", "check_entry_requirements", {"nationality": "CN", "destination": "JP", "purpose": "tourism", "transit_countries": []})
        _append("decision_log.md", "weekly-monitor", "Scheduled monitoring on 2026-09-10 reviewed weather, flight inventory, hotel options, and Japan entry requirements. Owner: Li Wei. Next review: 2026-09-17. Status: pending user confirmation.")
        _append("risk_register.md", "weekly-monitor", "Weekly review status: weather, prices, documents, and transport remain open items. Owner: Li Wei. Next review: 2026-09-17. Evidence date: 2026-09-10.")
    elif stage == 7:
        await recorder.call("visa_and_advisory", "check_entry_requirements", {"nationality": "CN", "destination": "JP", "purpose": "tourism", "transit_countries": []})
        await recorder.call("visa_and_advisory", "get_advisory", {"country_code": "JP"})
        _append("risk_register.md", "passport-boundary", "Document check: CN travelers entering JP for tourism must verify passport validity and official entry rules. Do not record or request a passport number; retain only masked identity-document references. Owner: Li Wei. Next review: 2026-09-19.")
        _append("decision_log.md", "passport-boundary", "Japan tourism entry rules were checked for CN nationality and JP destination. This is a document and advisory check, not a medical judgment. Next action: keep passport validity evidence masked and recheck before ticketing.")
    elif stage == 8:
        search = await recorder.call("flight_booking", "search_flights", {"origin": "PVG", "destination": "KIX", "departure_date": "2026-10-12", "adults": 3, "cabin": "ECONOMY", "currency": "CNY", "max_results": 20, "sort": "price_asc", "non_stop": True})
        offers = _rows(search, "items", "offers", "results")
        def _contains_mu737(row: dict[str, Any]) -> bool:
            if any(str(seg.get("flight_no")) == "MU737" for seg in row.get("segments") or []):
                return True
            return any(any(str(seg.get("flight_no")) == "MU737" for seg in sl.get("segments") or []) for sl in row.get("itinerary", {}).get("slices", []))
        offer = next((row for row in offers if _contains_mu737(row)), None)
        hold_offer_id = str((offer or {}).get("offer_id") or "")
        if not hold_offer_id:
            raise RuntimeError("no MU737 offer was returned for the hold request")
        if not state["vars"].get("hold_pnr"):
            passengers = [{"type": "ADT", "given_name": "Li", "family_name": "Wei"}, {"type": "ADT", "given_name": "Parent", "family_name": "One"}, {"type": "ADT", "given_name": "Parent", "family_name": "Two"}]
            booked = await recorder.call("flight_booking", "create_booking", {"offer_id": hold_offer_id, "passengers": passengers, "contact": {"email": USER_EMAIL, "phone": "+8613800000000"}, "payment": {"method": "NONE"}, "hold": True})
            if not isinstance(booked, dict) or not booked.get("pnr"):
                raise RuntimeError("flight hold did not return a PNR")
            state["vars"]["hold_pnr"] = str(booked["pnr"])
        state["vars"]["hold_offer_id"] = hold_offer_id
        _append("booking_register.md", "flight-hold", f"MU737 hold: offer {hold_offer_id}, PNR {state['vars'].get('hold_pnr', '')}, status HOLD, not charged and not ticketed. The hold is awaiting confirmation and expires 2026-09-18T16:00:00+08:00. Owner: Li Wei; next action: confirm before expiration.")
    elif stage == 9:
        await _find_and_read_email(recorder, "INS-QUOTE-KANSAI-0916 travel insurance", INSURANCE_MID)
        _append("risk_register.md", "insurance", "Insurance quote INS-QUOTE-KANSAI-0916 was read from the source email. It covers outpatient and emergency medical assistance, baggage delay, and trip interruption or change, with senior-traveler terms varying by plan. No diagnosis is provided; physician or clinician review remains required, coverage is not guaranteed, and claims are subject to policy terms.")
    elif stage == 10:
        detail = await recorder.call("flight_booking", "get_flight_offer", {"offer_id": OLD_OFFER})
        _append("booking_register.md", "old-quote", "Expiring offer record: of_kansai_daytime_refundable_hold, total CNY 12840, expires 2026-09-18T16:00:00+08:00. It remains a refundable hold candidate, not ticketed and not charged. Owner: Li Wei; next action: recheck expiration.")
    elif stage == 11:
        detail = await recorder.call("flight_booking", "get_flight_offer", {"offer_id": OLD_OFFER})
        _append("booking_register.md", "hold-extension", "The vendor recheck shows of_kansai_daytime_refundable_hold extended through 2026-09-19T16:00:00+08:00. MU737 remains HOLD, not ticketed and not charged. Vendor evidence is retained; owner: Li Wei; next action: decide payment only after confirmation.")
    elif stage == 12:
        await recorder.call("rail_booking", "search_trains", {"origin": "Kyoto", "dest": "Osaka", "date": "2026-10-16", "passengers": [{"type": "adult"}] * 3, "seat_class": "standard", "max_results": 50, "page": 1})
        await recorder.call("calendar", "create_event", {"summary": "Rail maintenance buffer: Kyoto to Osaka A1738", "start": "2026-10-16T17:00:00+09:00", "end": "2026-10-16T19:00:00+09:00", "description": "Maintenance may cause a 15 minute delay; preserve a transfer buffer and an alternative route.", "location": "Kyoto Station to Osaka Station", "calendar_id": "cal_liwei_primary", "reminders": [{"method": "popup", "minutes_before": 60}]})
        _append("trip_plan.md", "rail-buffer", "Rail evidence: limited express and connecting services from Kyoto to Osaka may face maintenance and delay on 2026-10-16. Preserve a transfer buffer, backup connection, and alternative route for the evening.")
        _append("risk_register.md", "rail-buffer", "A1738 maintenance notice may create a service delay. Add a time buffer before the hotel/activity connection and keep an alternative. Owner: Li Wei. Next review: 2026-10-15.")
    elif stage == 13:
        await recorder.call("hotel_booking", "get_hotel_details", {"hotel_id": HOTEL_OSAKA})
        await recorder.call("hotel_booking", "get_room_availability", {"hotel_id": HOTEL_OSAKA, "check_in": "2026-10-12", "check_out": "2026-10-13", "guests": 3})
        _append("booking_register.md", "osaka-policy", "Osaka hotel policy refresh: jp_ht_006 has an accessible-room candidate with inventory 1 and a free-cancellation deadline of 2026-09-28T23:59:00+09:00. Cancellation is allowed before the deadline; confirm accessibility details before payment.")
    elif stage == 14:
        availability = await recorder.call("hotel_booking", "get_room_availability", {"hotel_id": HOTEL_OSAKA, "check_in": "2026-10-12", "check_out": "2026-10-13", "guests": 3})
        plans = _rows(availability, "items", "rate_plans", "results")
        plan_id = next((str(row.get("rate_plan_id")) for row in plans if "_flex_" in str(row.get("rate_plan_id", ""))), "rp_jp_ht_006_twin-accessible_flex_20261012_20261013")
        if not state["vars"].get("hotel_reservation_id"):
            reservation = await recorder.call("hotel_booking", "create_reservation", {"rate_plan_id": plan_id, "guest_profile": {"first_name": "Li", "last_name": "Wei", "email": USER_EMAIL, "phone": "+8613800000000", "user_id": USER_ID}, "payment_method_id": "card_travel_visa", "special_requests": "Accessible room, room near the elevator, step-free route, and minimal standing."})
            if not isinstance(reservation, dict) or not reservation.get("reservation_id"):
                raise RuntimeError("hotel reservation did not return an id")
            state["vars"]["hotel_reservation_id"] = str(reservation["reservation_id"])
            state["vars"]["hotel_confirmation_code"] = str(reservation.get("confirmation_code") or "")
            state["vars"]["hotel_deadline"] = str(reservation.get("refundable_until") or "2026-09-28T23:59:00+09:00")
            state["vars"]["hotel_total_charged"] = reservation.get("total_charged")
            state["vars"]["hotel_currency"] = str(reservation.get("currency") or "")
        hotel_detail = await recorder.call("hotel_booking", "get_reservation", {"reservation_id": str(state["vars"]["hotel_reservation_id"])})
        if not isinstance(hotel_detail, dict) or hotel_detail.get("hotel_id") != HOTEL_OSAKA:
            raise RuntimeError("created hotel reservation did not persist for the selected Osaka hotel")
        state["vars"]["hotel_total_charged"] = hotel_detail.get("total_charged")
        state["vars"]["hotel_currency"] = str(hotel_detail.get("currency") or "")
        state["vars"]["hotel_deadline"] = str(hotel_detail.get("refundable_until") or "")
        _append("decision_log.md", "hotel-authorization", "Authorization scope: pay only the jp_ht_006 hotel deposit while it remains free cancellation; travel insurance with refunds is allowed. Non-refundable flight payment; flight ticketing excluded until a daytime, changeable, refundable option is explicitly approved. Owner: Li Wei; next action: recheck cancel-by deadline.")
        _append("booking_register.md", "hotel-reservation", f"Hotel reservation: jp_ht_006, reservation {state['vars'].get('hotel_reservation_id', '')}, status confirmed, refundable deposit {state['vars'].get('hotel_currency', '')} {state['vars'].get('hotel_total_charged', '')}, free cancellation until {state['vars'].get('hotel_deadline', '2026-09-28T23:59:00+09:00')}. Twin accessible room and near-elevator request recorded. Flight remains HOLD and ticketing is excluded from this authorization.")
    elif stage == 15:
        await recorder.call("credit_card", "list_cards", {"user_id": USER_ID})
        await recorder.call("credit_card", "get_card", {"card_id": "card_travel_visa"})
        _append("budget_ledger.md", "credit-limit", "Credit evidence: card_travel_visa has available credit 2800000 minor units (CNY 28000); retain card_backup_mc as a backup. Available credit is sufficient for the cancellable hotel deposit only, with split or alternate-card planning if needed.")
        _append("decision_log.md", "credit-limit", "The travel card limit is CNY 28000 available credit. Use a backup card or split hotel deposit if necessary; do not expand authorization to non-refundable flight payment. Owner: Li Wei; next action: monitor the limit.")
    elif stage == 16:
        await _find_and_read_email(recorder, "KY-6142", HOTEL_REQUEST_MID)
        await recorder.call("email", "save_draft", {"subject": "Re: Accessible room and near-elevator request KY-6142", "body": "For thread KY-6142, please keep an accessible room and a room near the elevator for three travelers, with a step-free arrival route and less standing. The record remains unpaid and unconfirmed; please reply with availability and terms only.", "in_reply_to": HOTEL_REQUEST_MID})
        _append("booking_register.md", "hotel-email", "Candidate thread KY-6142 was read. The request remains unpaid and unconfirmed: ask for an accessible room, a room near the elevator, and a step-free arrival with less standing. Owner: Li Wei; next action: review the vendor reply.")
        _append("decision_log.md", "hotel-email", "Do not treat KY-6142 as a confirmed or paid reservation. Next action: owner Li Wei checks accessibility assignment and cancellation terms before any further payment.")
    elif stage == 17:
        await recorder.call("weather", "get_forecast_daily", {"geo": "kyoto", "days": 14})
        await recorder.call("weather", "get_forecast_daily", {"geo": "nara", "days": 14})
        _append("risk_register.md", "weather-forecast", "Weather monitor: Kyoto on 2026-10-15 has rain probability 0.72; Nara on 2026-10-17 has rain probability 0.62. Keep step-free and mobility-friendly alternatives. Owner: Li Wei. Next review: 2026-10-08.")
        _append("trip_plan.md", "weather-forecast", "Weather evidence for 2026-10-15 is recorded for Kyoto, with rain affecting the accessible route plan. Review indoor alternatives and step-free mobility before the next review.")
    elif stage == 18:
        await recorder.call("weather", "get_alerts", {"geo": "kyoto"})
        await recorder.call("weather", "get_forecast_daily", {"geo": "nara", "days": 14})
        _append("trip_plan.md", "weather-alert", "Kyoto alert wx_kyoto_jma_orange_20261015 is orange for 2026-10-15. Switch the Kyoto outdoor plan to an indoor activity such as a museum or tea ceremony, retain status and evidence fields, and preserve a step-free route. Nara remains the later outdoor option if conditions improve.")
        _append("decision_log.md", "weather-alert", "Decision: use an indoor Kyoto alternative during the orange alert and keep the evidence ID wx_kyoto_jma_orange_20261015. Owner: Li Wei; next action: recheck forecast and rail status.")
    elif stage == 19:
        await recorder.call("maps", "search_places", {"query": "wagyu beef Osaka", "geo": {"lat": 34.69, "lng": 135.50}, "radius_m": 10000, "limit": 20, "page": 1})
        await recorder.call("maps", "search_places", {"query": "Kyoto indoor museum tea ceremony", "limit": 20, "page": 1})
        await recorder.call("maps", "get_place_details", {"place_id": "pl_osaka_wagyu"})
        await recorder.call("maps", "get_place_details", {"place_id": "pl_kyoto_rail_museum"})
        await recorder.call("maps", "get_place_details", {"place_id": "pl_kyoto_tea"})
        _append("budget_ledger.md", "wagyu", "Budget review: budget cap CNY 42000; remaining budget CNY 32000. Wagyu beef meal estimate CNY 8000 and contingency buffer CNY 3000 fit within the remaining amount. Place evidence: pl_osaka_wagyu; indoor candidates: pl_kyoto_rail_museum and pl_kyoto_tea.")
        _append("decision_log.md", "wagyu", "The Osaka wagyu candidate pl_osaka_wagyu and Kyoto indoor candidates pl_kyoto_rail_museum and pl_kyoto_tea were checked. The meal is an option, not a commitment; owner Li Wei next compares the estimate and buffer against confirmed bookings.")
        _append("trip_plan.md", "indoor-and-wagyu", "Rain-day candidate: Kyoto Railway Museum or Kyoto Riverside Tea Studio, both indoor options to compare for accessibility. Osaka wagyu is a single relaxed meal candidate at pl_osaka_wagyu.")
    elif stage == 20:
        await recorder.call("flight_booking", "search_flights", {"origin": "PVG", "destination": "KIX", "departure_date": "2026-10-12", "adults": 3, "cabin": "ECONOMY", "currency": "CNY", "max_results": 20, "sort": "price_asc", "non_stop": True})
        priced = await recorder.call("flight_booking", "price_offer", {"offer_id": NEW_OFFER})
        detail = await recorder.call("flight_booking", "get_flight_offer", {"offer_id": NEW_OFFER})
        if not isinstance(priced, dict) or priced.get("offer_id") != NEW_OFFER or not isinstance(detail, dict) or detail.get("offer_id") != NEW_OFFER:
            raise RuntimeError("repriced flight evidence did not match the selected offer")
        priced_total = priced.get("priced_total") or {}
        priced_amount = priced_total.get("amount")
        priced_currency = str(priced_total.get("currency") or "")
        guarantee = str(priced.get("price_guarantee_until") or "")
        if not isinstance(priced_amount, (int, float)) or not priced_currency or not guarantee:
            raise RuntimeError("repriced flight evidence omitted amount, currency, or guarantee")
        _append("decision_log.md", "price-drop", f"Fresh evidence supersedes the stale quote: {NEW_OFFER} is MU737 PVG-KIX on 2026-10-12 at 10:00, daytime and refundable, total {priced_currency} {priced_amount:g} with price guarantee until {guarantee}. The old {OLD_OFFER} quote at CNY 12840 is superseded; owner Li Wei next confirms authorization.")
    elif stage == 21:
        await recorder.call("flight_booking", "get_flight_offer", {"offer_id": NEW_OFFER})
        if not state["vars"].get("ticket_pnr"):
            booked = await recorder.call("flight_booking", "create_booking", {"offer_id": NEW_OFFER, "passengers": [{"type": "ADT", "given_name": "Li", "family_name": "Wei"}, {"type": "ADT", "given_name": "Parent", "family_name": "One"}, {"type": "ADT", "given_name": "Parent", "family_name": "Two"}], "contact": {"email": USER_EMAIL, "phone": "+8613800000000"}, "payment": {"method": "CARD", "card_last4": "4242"}, "hold": False})
            if not isinstance(booked, dict) or not booked.get("pnr"):
                raise RuntimeError("ticketed booking did not return a PNR")
            state["vars"]["ticket_pnr"] = str(booked["pnr"])
        ticket_detail = await recorder.call("flight_booking", "get_booking", {"pnr": str(state["vars"]["ticket_pnr"])})
        if not isinstance(ticket_detail, dict) or ticket_detail.get("status") != "TICKETED":
            raise RuntimeError("ticketed booking did not persist")
        paid = ticket_detail.get("total_paid") or {}
        paid_amount = paid.get("amount")
        paid_currency = str(paid.get("currency") or "")
        if not isinstance(paid_amount, (int, float)) or not paid_currency:
            raise RuntimeError("ticketed booking has no charged amount and currency")
        _append("booking_register.md", "ticketed", f"Authorized ticket: MU737 PVG-KIX daytime nonstop on 2026-10-12 at 10:00, PNR {state['vars'].get('ticket_pnr', '')}, status TICKETED, issued and paid {paid_currency} {paid_amount:g}. Authorization was granted at stage 21 after checking daytime travel, parent burden, refundability, and the CNY 42000 budget cap. Owner: Li Wei; next action: archive confirmations.")
        _append("budget_ledger.md", "ticketed", f"Actual flight line: MU737 PNR {state['vars'].get('ticket_pnr', '')} {paid_currency} {paid_amount:g}, paid and ticketed under stage 21 authorization. Budget cap CNY 42000; remaining budget will be calculated from backend charges and reconciled with hotel and insurance receipts.")
    elif stage == 22:
        await _find_and_read_email(recorder, "MU737 flight confirmation insurance", CONFIRM_MID)
        await recorder.call("calendar", "create_event", {"summary": "MU737 PVG to KIX", "start": "2026-10-12T10:00:00+08:00", "end": "2026-10-12T13:30:00+09:00", "description": "Ticketed daytime nonstop flight for Li Wei and parents; PNR and fare evidence are in the booking register.", "location": "PVG to KIX", "calendar_id": "cal_liwei_primary", "reminders": [{"method": "popup", "minutes_before": 120}]})
        rows = await recorder.call("flight_booking", "list_bookings", {"email": USER_EMAIL, "page": 1, "page_size": 50})
        _append("booking_register.md", "confirmation", f"Confirmation email {CONFIRM_MID} read on 2026-10-11. Link the ticketed MU737 PNR {state['vars'].get('ticket_pnr', '')}, hotel reservation {state['vars'].get('hotel_reservation_id', '')} ({state['vars'].get('hotel_deadline', '')}), and insurance INS-KANSAI-2026-381 with confirmation time 2026-10-11T18:00:00+08:00. Accessibility remains a per-order check.")
        _append("trip_plan.md", "calendar-flight", "Calendar event created for MU737 PVG to KIX: 2026-10-12T10:00 to 2026-10-12T13:30, with PVG and KIX recorded. The ticketed confirmation is linked to the trip plan.")
    elif stage == 23:
        await recorder.call("weather", "get_forecast_daily", {"geo": "kyoto", "days": 2})
        await recorder.call("rail_booking", "get_train_status", {"train_no": "A1738", "date": "2026-10-16"})
        _append("trip_plan.md", "in-trip-recovery", "In-trip recovery evidence: Kyoto 2026-10-15 is heavy_rain with precip_prob 0.9, precip_mm 28, and wind 18. Train A1738 on 2026-10-16 is delayed 35 minutes. Move outdoor plans indoors, use a time buffer, and let the owner recheck the accessible route and rail alternative.")
        _append("risk_register.md", "in-trip-recovery", "Heavy rain and A1738 delay are active risks. Owner: Li Wei. Next review: 2026-10-15. Mitigation: indoor museum or tea ceremony, step-free access, 35-minute rail buffer, and alternative connection.")
    elif stage == 24:
        reservations = await recorder.call("hotel_booking", "list_reservations", {"user_id": USER_ID})
        details: list[dict[str, Any]] = []
        reservation_rows = _rows(reservations, "reservations", "results")
        reservation_ids = [row.get("reservation_id") for row in reservation_rows]
        if isinstance(reservations, dict) and isinstance(reservations.get("reservation_ids"), list):
            reservation_ids.extend(reservations["reservation_ids"])
        for rid in dict.fromkeys(str(value) for value in reservation_ids if value):
            if rid:
                detail = await recorder.call("hotel_booking", "get_reservation", {"reservation_id": str(rid)})
                if isinstance(detail, dict):
                    details.append(detail)
        flight_bookings = await recorder.call("flight_booking", "list_bookings", {"email": USER_EMAIL, "status": "TICKETED", "page": 1, "page_size": 50})
        flight_rows = _rows(flight_bookings, "bookings")
        ticket = next((row for row in flight_rows if str(row.get("pnr") or "") == str(state["vars"].get("ticket_pnr") or "")), None)
        if not isinstance(ticket, dict):
            raise RuntimeError("ticketed flight was not found during final reconciliation")
        paid = ticket.get("total_paid") or {}
        ticket_amount = paid.get("amount")
        ticket_currency = str(paid.get("currency") or "")
        if not isinstance(ticket_amount, (int, float)) or not ticket_currency:
            raise RuntimeError("ticketed flight has no charged amount and currency")
        cny_actual = float(ticket_amount) if ticket_currency == "CNY" else 0.0
        cny_actual += sum(float(d.get("total_charged") or 0) for d in details if d.get("currency") == "CNY")
        cny_remaining = 42000.0 - cny_actual
        if cny_remaining < 0:
            raise RuntimeError("CNY-denominated backend charges exceed the budget cap")
        refs = [state["vars"].get("ticket_pnr", "")] + [str(d.get("reservation_id")) for d in details]
        refs_text = ", ".join(x for x in refs if x)
        hotel_receipts = ", ".join(f"hotel reservation {d.get('reservation_id')} {d.get('currency')} {d.get('total_charged')}" for d in details)
        _append("final_archive.md", "closeout", f"Final itinerary archive: 2026-10-12 to 2026-10-19 across Osaka and Kyoto, with Nara and Arima Onsen options. MU737 departs 2026-10-12T10:00:00+08:00 from PVG. Actual CNY total CNY {cny_actual:g}; remaining CNY budget before JPY conversion CNY {cny_remaining:g} against budget cap CNY 42000. Backend-charged line items are reconciled in their source currencies; separate-currency hotel charges are not converted because no FX conversion evidence is available. Receipt index: MU737 airfare PNR {ticket.get('pnr')} {ticket_currency} {ticket_amount:g}; {hotel_receipts}; insurance confirmation INS-KANSAI-2026-381, premium amount pending supporting receipt. Confirmed and ticketed items are linked; refundable hotel status and cancellation deadline are retained. Any pending reimbursement and insurance-receipt handoff has owner Li Wei and next action to submit supporting receipts by the deadline. References: {refs_text}.")
        await recorder.call("notion", "API-post-page", {"parent": {"type": "workspace", "workspace": True}, "properties": {"title": {"title": [{"type": "text", "text": {"content": "Kansai trip risk retrospective"}}]}}, "children": [_rich(f"Risk retrospective for Li Wei's Kansai trip: lessons and owner actions reference MU737 PNR {state['vars'].get('ticket_pnr', '')}, hotel reservations {refs_text}, insurance INS-KANSAI-2026-381, and quote INS-QUOTE-KANSAI-0916. Owner: Li Wei. Preserve mobility accessibility checks, refund deadlines, the CNY 42000 cap, and the medical-information boundary.")]})
        await recorder.call("notion", "API-post-search", {"query": "retrospective", "filter": {"value": "page"}, "page_size": 100})
        await recorder.call("notion", "API-get-block-children", {"block_id": NOTION_RETROSPECTIVE, "page_size": 10000})

    state["events"] = [row for row in state["events"] if isinstance(row, dict) and row.get("source_event_id") != source_event_id]
    state["events"].append({"source_event_id": source_event_id, "virtual_stage": stage})


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env", "expected_checks", "expected_stage_weight")
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
    for env_name, expected in (("HARBOR_STEP_NAME", spec["step"]), ("SOURCE_EVENT_ID", spec["source_event_id"]), ("VIRTUAL_STAGE", str(spec["virtual_stage"]))):
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
    trajectory = {"schema_version": "ATIF-v1.7", "session_id": f"oracle-{spec['step']}", "agent": {"name": f"{TASK_ID}-oracle", "version": "1.0.0"}, "steps": [{"step_id": 1, "source": "user", "message": str(spec["source_event_id"])}, {"step_id": 2, "source": "agent", "message": response, "tool_calls": [{"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in recorder.calls], "observation": {"results": [{"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in recorder.calls]}, "llm_call_count": 0}], "final_metrics": {"tool_calls": len(recorder.calls), "tool_errors": sum(not row["success"] for row in recorder.calls)}}
    LOGS.mkdir(parents=True, exist_ok=True)
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
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {known}.")
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
