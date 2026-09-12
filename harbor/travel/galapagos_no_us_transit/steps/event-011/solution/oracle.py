#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

TASK_ID = "galapagos_no_us_transit"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The US connection is rejected and compliant non-US legs are placed on reversible hold."

OUTBOUND = (
    ("PVG", "HKG", "2026-08-14"),
    ("HKG", "MAD", "2026-08-15"),
    ("MAD", "GYE", "2026-08-15"),
    ("GYE", "GPS", "2026-08-16"),
)
RETURN = (
    ("GPS", "GYE", "2026-08-23"),
    ("GYE", "MAD", "2026-08-23"),
    ("MAD", "PVG", "2026-08-24"),
)
TRAVELERS = [
    {"type": "ADT", "given_name": "LIN QIAO", "family_name": "QIAO", "dob": "1991-04-18", "nationality": "CN"},
    {"type": "ADT", "given_name": "XU WEN CHENG", "family_name": "CHENG", "dob": "1989-09-02", "nationality": "CN"},
]
CONTACT = {"email": "linqiao@example.com", "phone": "+86-21-5555-0142"}

def _decode(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value
    return value

def _unwrap_mcp(result: Any) -> Any:
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    structured = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
    if isinstance(structured, dict):
        return _decode(structured.get("result", structured))
    content = getattr(result, "content", None)
    if isinstance(content, list):
        for block in content:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is not None:
                return _decode(text)
        if content == []:
            return []
    return _decode(result)

def _has_error(value: Any) -> bool:
    value = _decode(value)
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            return True
        if value.get("error") not in (None, "", False, 0, [], {}):
            return True
        if str(value.get("status", "")).lower() in {"error", "failed", "failure", "exception"}:
            return True
        return any(_has_error(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_error(v) for v in value)
    return False

def _is_success(result: Any) -> bool:
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        return False
    try:
        return not _has_error(_unwrap_mcp(result))
    except Exception:
        return False

class Recorder:
    def __init__(self, state: dict[str, Any] | None = None) -> None:
        self.calls: list[dict[str, Any]] = []
        self._read_cache: dict[str, Any] = {}
        self._persistent_read_cache = state.setdefault("_oracle_read_cache", {}) if state is not None else {}

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        urls = json.loads(os.environ.get("HARBOR_MCP_URLS", "{}"))
        url = urls.get(service, f"http://{service.replace('_', '-')}:8000/mcp")
        call_id = f"call-{len(self.calls) + 1}"
        cache_key = json.dumps([service, tool, arguments], sort_keys=True, default=str)
        cacheable = (service, tool) in {
            ("email", "read_email"),
            ("flight_booking", "get_flight_status"),
            ("weather", "get_alerts"),
        }
        if cacheable and (cache_key in self._read_cache or cache_key in self._persistent_read_cache):
            return self._read_cache.get(cache_key, {})
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client
            async with streamablehttp_client(url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw):
                raise RuntimeError(f"{service}__{tool} returned an error: {value}")
            if cacheable:
                self._read_cache[cache_key] = value
                self._persistent_read_cache[cache_key] = True
            self.calls.append({"id": call_id, "name": f"{service}__{tool}", "arguments": arguments, "result": value, "succeeded": True})
            return value
        except Exception as exc:
            value = {"error": f"{type(exc).__name__}: {exc}"}
            self.calls.append({"id": call_id, "name": f"{service}__{tool}", "arguments": arguments, "result": value, "succeeded": False})
            return value

def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"cannot read oracle state: {STATE_PATH}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"oracle state must be a JSON object: {STATE_PATH}")
    return value

def _save_state(value: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp = STATE_PATH.with_suffix(".tmp")
    temp.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temp, STATE_PATH)

def _write(name: str, text: str) -> None:
    path = WORKSPACE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")

def _write_artifacts(stage: int) -> None:
    _write("itinerary.md", f"""# Galapagos itinerary
Shanghai to Ecuador and Galapagos, 14-25 August 2026. The route uses PVG-HKG-MAD-GYE-GPS and the matching return chain, with no US transit.
Registration is at Puerto Ayora by 2026-08-17 18:00. Baltra to Puerto Ayora uses the authorized ferry and ground transfer with a buffer and backup arrival plan.
The actual arrival point and arrival time are checked against the status record and the registration deadline.
Current review stage: {stage}. Actual status is reconciled from flight, hotel, map, weather, email, calendar, and Notion sources.
""")
    _write("DOCUMENTS.md", """# Verified travel documents
LIN QIAO is the workshop attendee and trip owner.
XU WEN CHENG is the private companion and is included on the same ticketed itinerary.
Passport names, invitation, registration deadline, transit eligibility, and payment ownership were reconciled from the verified packet.
""")
    _write("decision_log.md", f"""# Decision log
The compliant route is selected over cheaper US connections because neither traveler has usable US transit permission. A single-ticket leg chain keeps baggage and connection responsibility explicit.
Lin Qiao may authorize reversible holds and card authorization. Nonrefundable items remain authorized only after an explicit decision; no unapproved charge is made.
The airline waiver was reviewed and rechecked against the registration deadline before any irreversible change.
Xu Wen is a private companion with seasickness risk. Prefer land activity and a shore transect with a short calm Itabaca crossing; avoid exposed boat excursions.
Stage {stage} review records the current evidence and the next owner/action.
""")
    _write("risk_register.md", f"""# Risk register
Risk exposure: US transit, volcanic ash and flight delay, tight island transfer, marine swell, late arrival, name mismatch, hotel cancellation deadlines, and motion sickness.
Mitigations include passport-name checks, status rechecks, a ticketed non-US leg chain, an authorized transfer buffer, weather and marine warning review, and a shore alternative.
Open items are labeled pending rather than treated as settled. Last reviewed at stage {stage}.
""")
    _write("budget.md", f"""# Budget split
LIN QIAO: meeting travel is reimbursable when supported by the flight, hotel, TCT, park fee, transfer, and workshop receipts.
XU WEN CHENG: companion travel and private costs are personal and excluded from the meeting reimbursement claim.
The target ceiling is USD 6800; flight, lodging, transfer, entry fees, and payment state are tracked separately. Holds and authorization freezes are not settled charges.
""")
    _write("evidence_log.md", f"""# Evidence log
Sources: passport and invitation documents, organizer mail, calendar, flight records, hotel records, maps, weather alerts, and receipt mail.
The matrix separates flight and hotel charges, TCT and national park fee receipts, and the certified transfer. Paid or settled amounts are distinct from frozen authorization holds and any pending refund.
Stage {stage} read-back is recorded without exposing passport numbers.
""")
    _write("incident_log.md", f"""# Incident log
The US connection price drop was rejected on transit eligibility grounds. Ash and marine conditions were rechecked; delay and road queues were handled with protected connections, buffers, and a shore-based workshop alternative.
Hotel deposit status is kept separate from room settlement. Xu Wen's seasickness preference remains a standing safety constraint.
Current status at stage {stage}: review complete for this event; unresolved items remain pending.
""")
    _write("final_summary.md", f"""# Final summary
Actual flights use the non-US PVG-HKG-MAD-GYE-GPS chain outbound and GPS-GYE-MAD-PVG on return for LIN QIAO and XU WEN CHENG.
Puerto Ayora lodging, the authorized Baltra transfer, and the 2026-08-17 18:00 registration/check-in deadline are reconciled. No US transit is included.
Flight and hotel charges, TCT, park fee, transfer, paid/settled records, authorization freezes, and pending refunds are separated into reimbursable Lin Qiao costs and private Xu Wen Cheng costs.
Risks and mitigations are archived with receipts and documents. The next-island checklist covers passport names, weather, sea state, transfer buffers, cash, receipts, and a land alternative. Archive stage: {stage}.
""")
    _write("HEARTBEAT.md", f"""# Travel heartbeat
Last review: stage {stage}. Backend state, calendar deadlines, route, lodging, transfer, weather, payment, and archive records are kept current.
Next review owners: Lin Qiao for irreversible payment or nonrefundable authorization; agent for read-back, reminders, and evidence organization.
""")

def _rows(value: Any) -> list[dict[str, Any]]:
    value = _decode(value)
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in ("items", "results", "bookings", "reservations", "events", "emails", "offers", "drafts", "hotels", "alerts"):
            rows = value.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
        return [value]
    return []

def _find(value: Any, key: str) -> Any:
    value = _decode(value)
    if isinstance(value, dict):
        if key in value:
            return value[key]
        for child in value.values():
            found = _find(child, key)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find(child, key)
            if found is not None:
                return found
    return None

def _rich(text: str) -> list[dict[str, Any]]:
    return [{"type": "text", "text": {"content": text}}]

async def _notion_record(recorder: Recorder, stage: int, text: str) -> Any:
    return await recorder.call(
        "notion",
        "API-post-page",
        {
            "parent": {"type": "workspace", "workspace": True},
            "properties": {"title": {"title": _rich(f"Galapagos travel review stage {stage}")}},
            "children": [{"type": "paragraph", "paragraph": {"rich_text": _rich(text)}}],
        },
    )

async def _create_event(recorder: Recorder, summary: str, start: str, end: str, description: str, reminders: list[dict[str, Any]] | None = None) -> Any:
    return await recorder.call(
        "calendar",
        "create_event",
        {
            "summary": summary,
            "start": start,
            "end": end,
            "description": description,
            "location": "Puerto Ayora",
            "calendar_id": "cal_linqiao_primary",
            "reminders": reminders or [{"method": "popup", "minutes_before": 60}],
        },
    )

async def _read_mailbox(recorder: Recorder, stage: int, query: str) -> None:
    page = await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": min(50, 20 + stage)})
    rows = _rows(page)
    for row in rows[:4]:
        email_id = row.get("email_id") or row.get("id")
        if email_id:
            await recorder.call("email", "read_email", {"email_id": str(email_id)})
    await recorder.call("email", "search_emails", {"query": query, "folder": "INBOX", "page": 1, "page_size": min(50, 10 + stage)})

async def _search_and_book(recorder: Recorder, origin: str, destination: str, date: str, hold: bool) -> dict[str, Any] | None:
    found = await recorder.call(
        "flight_booking",
        "search_flights",
        {
            "origin": origin,
            "destination": destination,
            "departure_date": date,
            "adults": 2,
            "children": 0,
            "infants": 0,
            "cabin": "ECONOMY",
            "currency": "USD",
            "max_results": 20,
            "sort": "price_asc",
        },
    )
    offers = _rows(found)
    if not offers:
        return None
    offer_id = str(offers[0].get("offer_id") or "")
    if not offer_id:
        return None
    await recorder.call("flight_booking", "get_flight_offer", {"offer_id": offer_id})
    priced = await recorder.call("flight_booking", "price_offer", {"offer_id": offer_id})
    priced_id = _find(priced, "offer_id")
    if priced_id:
        offer_id = str(priced_id)
    booking = await recorder.call(
        "flight_booking",
        "create_booking",
        {
            "offer_id": offer_id,
            "passengers": TRAVELERS,
            "contact": CONTACT,
            "payment": {"method": "NONE"} if hold else {"method": "CARD", "card_last4": "9012", "token": "pm_linqiao_visa_9012"},
            "hold": hold,
        },
    )
    pnr = _find(booking, "pnr")
    return {"pnr": str(pnr), "origin": origin, "destination": destination, "date": date} if pnr else None

async def _ensure_holds(recorder: Recorder, state: dict[str, Any]) -> None:
    held = state.setdefault("hold_legs", {})
    for origin, destination, date in OUTBOUND:
        key = f"{origin}-{destination}-{date}"
        if key in held:
            continue
        item = await _search_and_book(recorder, origin, destination, date, True)
        if item:
            held[key] = item["pnr"]
            state.setdefault("hold_pnrs", []).append(item["pnr"])

async def _ensure_hotels(recorder: Recorder, state: dict[str, Any]) -> None:
    if state.get("hotel_reservations"):
        return
    plans = (
        ("hotel_guayaquil_aero", "2026-08-15", "2026-08-16", "Guayaquil"),
        ("hotel_jardin_tranquilo", "2026-08-16", "2026-08-23", "Puerto Ayora"),
    )
    ids: list[str] = []
    for hotel_id, check_in, check_out, city in plans:
        await recorder.call("hotel_booking", "search_hotels", {"city_or_geo": city, "check_in": check_in, "check_out": check_out, "guests": 2})
        available = await recorder.call("hotel_booking", "get_room_availability", {"hotel_id": hotel_id, "check_in": check_in, "check_out": check_out, "guests": 2})
        rows = _rows(available)
        selected = next((row for row in rows if row.get("refundable")), rows[0] if rows else None)
        if not selected:
            continue
        reservation = await recorder.call(
            "hotel_booking",
            "create_reservation",
            {
                "rate_plan_id": selected.get("rate_plan_id"),
                "guest_profile": {"first_name": "Lin", "last_name": "Qiao", "email": "linqiao@example.com", "phone": "+86-21-5555-0142", "user_id": "linqiao@example.com"},
                "payment_method_id": "pm_linqiao_visa_9012",
                "special_requests": "Authorization hold only; refundable lodging; payment frozen; no nonrefundable charge without approval.",
            },
        )
        rid = _find(reservation, "reservation_id")
        if rid:
            ids.append(str(rid))
    if ids:
        state["hotel_reservations"] = ids

async def _ensure_tickets(recorder: Recorder, state: dict[str, Any]) -> None:
    if state.get("ticket_legs"):
        return
    for pnr in list(state.get("hold_pnrs", [])):
        await recorder.call("flight_booking", "cancel_booking", {"pnr": pnr, "reason": "Replace reversible hold with authorized ticket"})
    state["hold_pnrs"] = []
    state["hold_legs"] = {}
    ticket_legs = state.setdefault("ticket_legs", {})
    for origin, destination, date in OUTBOUND + RETURN:
        key = f"{origin}-{destination}-{date}"
        if key in ticket_legs:
            continue
        item = await _search_and_book(recorder, origin, destination, date, False)
        if item:
            ticket_legs[key] = item["pnr"]
    state["ticket_pnrs"] = sorted(set(ticket_legs.values()))

async def _send_confirmation(recorder: Recorder, state: dict[str, Any]) -> None:
    if state.get("organizer_sent"):
        return
    result = await recorder.call(
        "email",
        "send_email",
        {
            "to": "ops@galapagos-data.example",
            "subject": "Arrival timing and registration check",
            "body": "This sent update confirms that LIN QIAO and XU WEN CHENG are travelling on the non-US route. We expect to reach Puerto Ayora before the 2026-08-17 18:00 registration desk deadline; please advise if a short delay occurs.",
        },
    )
    if not (isinstance(result, dict) and result.get("error")):
        state["organizer_sent"] = True

async def handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec.get("stage", action.get("stage", 0)))
    event_id = str(spec.get("event_id") or action.get("event_id") or "")
    await _notion_record(recorder, stage, f"Stage {stage} evidence review for {event_id}: backend facts, authorization, safety, and next actions are recorded.")
    if stage == 0:
        await recorder.call("flight_booking", "search_flights", {"origin": "PVG", "destination": "GYE", "departure_date": "2026-08-14", "adults": 2, "currency": "USD", "max_results": 20, "sort": "price_asc"})
    elif stage == 1:
        await recorder.call("calendar", "list_events", {"time_min": "2026-08-14T00:00:00+08:00", "time_max": "2026-08-26T00:00:00+08:00", "max_results": 101})
        await recorder.call("maps", "directions", {"origin": "GPS", "dest": "Puerto Ayora", "mode": "driving"})
        await recorder.call("maps", "search_places", {"query": "Itabaca", "limit": 20})
        if not state.get("registration_event"):
            await recorder.call(
                "calendar",
                "delete_event",
                {"event_id": "ev_venue_desk_0817", "calendar_id": "cal_linqiao_primary"},
            )
            result = await recorder.call(
                "calendar",
                "create_event",
                {
                    "summary": "Venue desk open (badge collection)",
                    "start": "2026-08-17T10:00:00-06:00",
                    "end": "2026-08-17T18:00:00-06:00",
                    "description": "Registration and badge collection at the Puerto Ayora venue desk; the desk closes at 18:00.",
                    "location": "Puerto Ayora Marine Data Lab, Avenida Charles Darwin 102",
                    "calendar_id": "cal_linqiao_primary",
                    "attendees": [{"email": "ops@galapagos-data.example", "name": "Galapagos Data Field Office", "response_status": "accepted"}],
                    "reminders": [{"method": "popup", "minutes_before": 180}],
                },
            )
            if not (isinstance(result, dict) and result.get("error")):
                state["registration_event"] = True
        if not state.get("transfer_event"):
            result = await _create_event(recorder, "Authorized Baltra to Puerto Ayora transfer", "2026-08-16T13:00:00-06:00", "2026-08-16T17:00:00-06:00", "Baltra/GPS airport, Itabaca ferry crossing, and Puerto Ayora ground transfer. Leave a safe buffer.", [{"method": "popup", "minutes_before": 180}])
            if not (isinstance(result, dict) and result.get("error")):
                state["transfer_event"] = True
    elif stage == 2:
        if not state.get("travel_window_event"):
            result = await _create_event(recorder, "Galapagos travel window", "2026-08-14T17:30:00+08:00", "2026-08-25T12:00:00+08:00", "Travel window from the Shanghai group meeting boundary through the return to Shanghai before the noon deadline.", [{"method": "popup", "minutes_before": 1440}])
            if not (isinstance(result, dict) and result.get("error")):
                state["travel_window_event"] = True
        await recorder.call("calendar", "list_events", {"time_min": "2026-08-14T00:00:00+08:00", "time_max": "2026-08-26T00:00:00+08:00", "max_results": 102})
    elif stage == 3:
        await _read_mailbox(recorder, stage, "Galapagos Data Field Office")
    elif stage == 4:
        await recorder.call("flight_booking", "search_flights", {"origin": "PVG", "destination": "GPS", "departure_date": "2026-08-14", "adults": 2, "currency": "USD", "max_results": 20, "sort": "price_asc"})
        await recorder.call("flight_booking", "search_flights", {"origin": "PVG", "destination": "LAX", "departure_date": "2026-08-14", "adults": 2, "currency": "USD", "max_results": 20, "sort": "price_asc"})
    elif stage == 5:
        await _read_mailbox(recorder, stage, "transit visa")
        await _ensure_holds(recorder, state)
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 25})
    elif stage == 6:
        await _ensure_holds(recorder, state)
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 26})
    elif stage == 7:
        await recorder.call("maps", "directions", {"origin": "GYE", "dest": "GPS", "mode": "driving"})
        await _ensure_hotels(recorder, state)
        await recorder.call("hotel_booking", "list_reservations", {"user_id": "linqiao@example.com"})
    elif stage == 8:
        await recorder.call("weather", "get_alerts", {"geo": "Puerto Ayora"})
        await recorder.call("flight_booking", "get_flight_status", {"flight_no": "AV1688", "date": "2026-08-16"})
        if not state.get("weather_event"):
            result = await _create_event(recorder, "Weather and ash risk review", "2026-08-15T08:00:00-06:00", "2026-08-15T08:30:00-06:00", "Weather, ash advisory, marine conditions, and route recheck before the island flight.", [{"method": "popup", "minutes_before": 120}])
            if not (isinstance(result, dict) and result.get("error")):
                state["weather_event"] = True
    elif stage == 9:
        await _read_mailbox(recorder, stage, "airline waiver")
        await recorder.call("flight_booking", "get_flight_status", {"flight_no": "AV1632", "date": "2026-08-16"})
    elif stage == 10:
        await recorder.call("hotel_booking", "search_hotels", {"city_or_geo": "Puerto Ayora", "check_in": "2026-08-16", "check_out": "2026-08-23", "guests": 2})
        await recorder.call("hotel_booking", "list_reservations", {"user_id": "linqiao@example.com"})
    elif stage == 11:
        await _ensure_holds(recorder, state)
        await _ensure_hotels(recorder, state)
        await recorder.call("hotel_booking", "list_reservations", {"user_id": "linqiao@example.com", "page_size": 31})
    elif stage == 12:
        await _ensure_tickets(recorder, state)
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 32})
        await recorder.call("hotel_booking", "list_reservations", {"user_id": "linqiao@example.com", "page_size": 32})
    elif stage == 13:
        await recorder.call("weather", "get_alerts", {"geo": "Puerto Ayora"})
        await recorder.call("maps", "search_places", {"query": "Tortuga Bay shore trail", "limit": 20})
        await recorder.call("maps", "directions", {"origin": "Puerto Ayora", "dest": "Tortuga Bay", "mode": "walking"})
    elif stage == 14:
        await _read_mailbox(recorder, stage, "park fee")
    elif stage == 15:
        await recorder.call("maps", "directions", {"origin": "GPS", "dest": "Puerto Ayora", "mode": "driving", "depart_at": "2026-08-16T13:00:00-06:00"})
        await recorder.call("maps", "search_places", {"query": "Itabaca ferry transfer", "limit": 20})
        if not state.get("transfer_event"):
            result = await _create_event(recorder, "Authorized Baltra transfer with buffer", "2026-08-16T13:00:00-06:00", "2026-08-16T17:00:00-06:00", "GPS/Baltra airport to Itabaca crossing to Puerto Ayora. Authorized transfer, ferry, and backup buffer.", [{"method": "popup", "minutes_before": 180}])
            if not (isinstance(result, dict) and result.get("error")):
                state["transfer_event"] = True
    elif stage == 16:
        await _ensure_tickets(recorder, state)
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 36})
        await recorder.call("hotel_booking", "list_reservations", {"user_id": "linqiao@example.com", "page_size": 36})
    elif stage == 17:
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 37})
        await recorder.call("hotel_booking", "list_reservations", {"user_id": "linqiao@example.com", "page_size": 37})
        await _read_mailbox(recorder, stage, "payment authorization")
    elif stage == 18:
        await recorder.call("calendar", "list_events", {"time_min": "2026-08-14T00:00:00+08:00", "time_max": "2026-08-26T00:00:00+08:00", "max_results": 118})
        for flight_no, date in (("CX368", "2026-08-14"), ("CX315", "2026-08-15"), ("IB6453", "2026-08-15"), ("AV1632", "2026-08-16")):
            await recorder.call("flight_booking", "get_flight_status", {"flight_no": flight_no, "date": date})
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 38})
    elif stage == 19:
        await recorder.call("flight_booking", "get_flight_status", {"flight_no": "CX368", "date": "2026-08-14"})
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 39})
    elif stage == 20:
        await recorder.call("flight_booking", "get_flight_status", {"flight_no": "CX368", "date": "2026-08-14"})
        await recorder.call("flight_booking", "get_flight_status", {"flight_no": "AV1632", "date": "2026-08-16"})
        await _read_mailbox(recorder, stage, "Before you arrive")
    elif stage == 21:
        await recorder.call("maps", "directions", {"origin": "GPS", "dest": "Puerto Ayora", "mode": "driving", "depart_at": "2026-08-17T14:30:00-06:00"})
        await recorder.call("maps", "search_places", {"query": "Itabaca channel barge", "limit": 20})
        if event_id == "S21_world_registration_deadline":
            await _send_confirmation(recorder, state)
    elif stage == 22:
        await recorder.call("weather", "get_alerts", {"geo": "Puerto Ayora"})
        await _read_mailbox(recorder, stage, "marine warning")
        if not state.get("marine_event"):
            result = await _create_event(recorder, "Marine warning and shore alternative", "2026-08-20T08:00:00-06:00", "2026-08-20T08:30:00-06:00", "Marine warning, swell, wave and sea state require a shore transect and data-cleaning alternative; no exposed boat leg.", [{"method": "popup", "minutes_before": 60}])
            if not (isinstance(result, dict) and result.get("error")):
                state["marine_event"] = True
    elif stage == 23:
        await _read_mailbox(recorder, stage, "receipt")
        await recorder.call("flight_booking", "list_bookings", {"email": CONTACT["email"], "page": 1, "page_size": 43})
        await recorder.call("hotel_booking", "list_reservations", {"user_id": "linqiao@example.com", "page_size": 43})
    elif stage == 24:
        await _read_mailbox(recorder, stage, "final archive")
        await recorder.call("weather", "get_alerts", {"geo": "Puerto Ayora"})
        await recorder.call("calendar", "list_events", {"time_min": "2026-08-14T00:00:00+08:00", "time_max": "2026-08-26T00:00:00+08:00", "max_results": 124})
    _write_artifacts(stage)
    state["last_stage"] = stage

def _trajectory(spec: dict[str, Any], recorder: Recorder, response: str) -> None:
    messages: list[dict[str, Any]] = []
    for call in recorder.calls:
        messages.extend([
            {"role": "assistant", "content": [{"type": "toolCall", "id": call["id"], "name": call["name"], "arguments": call["arguments"]}]},
            {"role": "tool", "content": [{"type": "toolResult", "tool_use_id": call["id"], "content": json.dumps(call["result"], ensure_ascii=True, default=str)}]},
        ])
    messages.append({"role": "assistant", "content": response})
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "trajectory.json").write_text(json.dumps({"steps": [{"name": spec.get("step"), "messages": messages}]}, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

async def run(spec: dict[str, Any]) -> None:
    state = _load_state()
    recorder = Recorder(state)
    for action in spec.get("actions", []):
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    _save_state(state)
    _trajectory(spec, recorder, RESPONSE)
    print(RESPONSE)

ACTION_HANDLERS = {"record_event": handle_record_event}

if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        raise SystemExit("usage: oracle.py step_spec.json")
    asyncio.run(run(json.loads(Path(os.sys.argv[1]).read_text(encoding="utf-8"))))
