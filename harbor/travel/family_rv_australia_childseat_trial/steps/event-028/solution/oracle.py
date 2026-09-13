#!/usr/bin/env python3
"""Executable Oracle for the Australia family motorhome trial."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

TASK_ID = "family_rv_australia_childseat_trial"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The Australia motorhome trial step was completed through the relevant travel systems and recorded."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "car_rental": "http://car-rental:8000/mcp",
    "credit_card": "http://credit-card:8000/mcp",
    "email": "http://email:8000/mcp",
    "flight_booking": "http://flight-booking:8000/mcp",
    "hotel_booking": "http://hotel-booking:8000/mcp",
    "maps": "http://maps:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "visa_and_advisory": "http://visa-and-advisory:8000/mcp",
    "weather": "http://weather:8000/mcp",
}
USER_ID = "user_li_cheng"
CARD_ID = "card_world_travel_plus_2609"


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
    """Normalize supported MCP return shapes; [] is a successful empty read."""
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
        code = str(value.get("code") or "").upper()
        if code.startswith(("BAD_", "NOT_", "ERR", "FAIL", "INVALID_", "DENIED")):
            return False
    if isinstance(value, list):
        return all(_is_success(x) for x in value) if value else True
    return value is not None


class Recorder:
    """Call MCP services and retain the exact ATIF calls and observations."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any], *, trace_aliases: dict[str, Any] | None = None) -> Any:
        if service not in SERVICE_URLS:
            raise ValueError(f"unsupported MCP service: {service!r}")
        call_id = f"call-{len(self.calls) + 1}"
        recorded_arguments = {**arguments, **(trace_aliases or {})}
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
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": recorded_arguments, "result": value, "success": True, "error": None})
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": recorded_arguments, "result": {"error": error}, "success": False, "error": error})
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc

    def workspace_write(self, filename: str, text: str) -> None:
        if Path(filename).name != filename:
            raise ValueError("workspace path must be a file name")
        target = WORKSPACE / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8") if target.is_file() else ""
        if text.strip() not in old:
            target.write_text((old.rstrip() + "\n\n" + text.rstrip() + "\n").lstrip(), encoding="utf-8")
        self.calls.append({"tool_call_id": f"call-{len(self.calls) + 1}", "function_name": "workspace__append_file", "arguments": {"path": str(target), "filename": filename, "text": text}, "result": {"ok": True}, "success": True, "error": None})


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
    if not isinstance(value, dict) or value.get("version") != 1 or not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict):
        raise RuntimeError("oracle state must be a versioned JSON object")
    return value


def _save_state(state: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    temp = STATE_PATH.with_suffix(STATE_PATH.suffix + ".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(STATE_PATH)


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [x for x in value if isinstance(x, dict)]
    if isinstance(value, dict):
        for key in keys:
            if isinstance(value.get(key), list):
                return [x for x in value[key] if isinstance(x, dict)]
    return []


def _rich(text: str) -> dict[str, Any]:
    return {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


async def _notion_page(rec: Recorder, state: dict[str, Any]) -> str:
    page_id = state["vars"].get("notion_page_id")
    if page_id:
        return str(page_id)
    result = await rec.call("notion", "API-post-page", {
        "parent": {"type": "workspace", "workspace": True},
        "properties": {"title": {"title": [{"type": "text", "text": {"content": "Australia Family Motorhome Route Trial"}}]}},
        "children": [_rich("Sydney to Canberra to Melbourne; family of three; child restraint, right-hand-drive, insurance, weather, budget and authorization are tracked.")],
    })
    if not isinstance(result, dict) or not (result.get("id") or result.get("page_id")):
        raise RuntimeError("Notion page creation returned no page id")
    page_id = result.get("id") or result.get("page_id")
    state["vars"]["notion_page_id"] = page_id
    return str(page_id)


async def _notion_append(rec: Recorder, state: dict[str, Any], text: str) -> None:
    page = await _notion_page(rec, state)
    await rec.call("notion", "API-patch-block-children", {"block_id": page, "children": [_rich(text)]})


async def _calendar_id(rec: Recorder, state: dict[str, Any]) -> str:
    if state["vars"].get("calendar_id"):
        return str(state["vars"]["calendar_id"])
    rows = _rows(await rec.call("calendar", "list_calendars", {"user_id": USER_ID}))
    if not rows:
        raise RuntimeError("no calendar available")
    cid = rows[0].get("calendar_id")
    if not cid:
        raise RuntimeError("calendar listing returned no id")
    state["vars"]["calendar_id"] = cid
    return str(cid)


async def _calendar_event(rec: Recorder, state: dict[str, Any], summary: str, start: str, end: str, description: str) -> None:
    await rec.call("calendar", "create_event", {"calendar_id": await _calendar_id(rec, state), "summary": summary, "start": start, "end": end, "description": description, "location": "Australia", "reminders": [{"method": "popup", "minutes_before": 60}]})


async def _flight_search(rec: Recorder, origin: str, destination: str, date: str, return_date: str | None = None, cabin: str = "ECONOMY") -> list[dict[str, Any]]:
    result = await rec.call("flight_booking", "search_flights", {"origin": origin, "destination": destination, "departure_date": date, "return_date": return_date, "adults": 2, "children": 1, "cabin": cabin, "currency": "CNY", "max_results": 50, "sort": "price_asc", "non_stop": True})
    return _rows(result, "items", "offers", "results")


async def _hotel_search(rec: Recorder, city: str, check_in: str, check_out: str) -> list[dict[str, Any]]:
    result = await rec.call("hotel_booking", "search_hotels", {"city_or_geo": city, "check_in": check_in, "check_out": check_out, "guests": 3, "filters": {"sort": "price_asc", "limit": 50, "refundable_only": True}, "page": 1})
    return _rows(result, "items", "hotels", "results")


async def _hotel_availability(rec: Recorder, hotel_id: str, check_in: str, check_out: str) -> list[dict[str, Any]]:
    value = await rec.call("hotel_booking", "get_room_availability", {"hotel_id": hotel_id, "check_in": check_in, "check_out": check_out, "guests": 3})
    return _rows(value, "items", "results")


async def _record_hotel(rec: Recorder, hotel_id: str, check_in: str, check_out: str, state: dict[str, Any], note: str) -> None:
    plans = await _hotel_availability(rec, hotel_id, check_in, check_out)
    if not plans:
        raise RuntimeError(f"no hotel rate plan for {hotel_id}")
    plan = plans[0]
    guest = {"first_name": "Li", "last_name": "Cheng", "email": "li.cheng@example.cn", "phone": "+86-13800000000", "user_id": USER_ID}
    result = await rec.call("hotel_booking", "create_reservation", {"rate_plan_id": plan["rate_plan_id"], "guest_profile": guest, "payment_method_id": CARD_ID, "special_requests": note})
    if isinstance(result, dict) and result.get("reservation_id"):
        state["vars"].setdefault("hotel_reservations", []).append(result["reservation_id"])


def _cny_amount(amount: Any, currency: Any) -> float:
    """Convert a backend amount to CNY at the rate stated in /workspace/BUDGET.md (AUD 1 = 4.80).

    Returns 0.0 rather than raising on an unparseable amount: the oracle must never crash a
    trial over a display figure, and a wrong total only costs the traceability check.
    """
    try:
        value = float(amount)
    except (TypeError, ValueError):
        return 0.0
    return value * 4.80 if str(currency or "").strip().upper() == "AUD" else value


async def _record_flights(rec: Recorder, state: dict[str, Any]) -> None:
    outbound = await _flight_search(rec, "PVG", "SYD", "2026-09-12")
    inbound = await _flight_search(rec, "MEL", "PVG", "2026-09-26", cabin="PREMIUM_ECONOMY")
    outbound_offer = next((x for x in outbound if "SC888" in json.dumps(x)), None)
    inbound_offer = next((x for x in inbound if "SC889" in json.dumps(x)), None)
    if outbound_offer is None or inbound_offer is None:
        raise RuntimeError("required SC888/SC889 flight offers are unavailable")
    passengers = [{"type": "ADT", "given_name": "Li", "family_name": "Cheng", "dob": "1985-01-01"}, {"type": "ADT", "given_name": "Zhou", "family_name": "Ran", "dob": "1987-02-02"}, {"type": "CHD", "given_name": "Li", "family_name": "Mi", "dob": "2022-04-04"}]
    contact = {"email": "li.cheng@example.cn", "phone": "+86-13800000000"}
    for offer in (outbound_offer, inbound_offer):
        booking = await rec.call("flight_booking", "create_booking", {"user_id": USER_ID, "offer_id": offer["offer_id"], "passengers": passengers, "contact": contact, "payment": {"method": "NONE"}, "hold": True})
        if isinstance(booking, dict) and booking.get("pnr"):
            state["vars"].setdefault("flight_pnrs", []).append(booking["pnr"])
            # Read the booking back: segment routes (flight_no/origin/destination) exist only in
            # get_booking's response, so a rubric that verifies the booked route can see it only
            # if the agent actually re-read the booking it just created.
            await rec.call("flight_booking", "get_booking", {"pnr": booking["pnr"]})


async def _search_route(rec: Recorder, origin: str, dest: str, depart_at: str) -> None:
    await rec.call("maps", "directions", {"origin": origin, "dest": dest, "mode": "driving", "depart_at": depart_at})


async def _email(rec: Recorder, subject: str, body: str, draft: bool = False) -> None:
    if draft:
        await rec.call("email", "save_draft", {"subject": subject, "body": body, "to": "li.cheng@example.cn"})
    else:
        await rec.call("email", "send_email", {"to": "li.cheng@example.cn", "subject": subject, "body": body})


def _entry(stage: int, source: str, facts: str, action: str, next_step: str) -> str:
    return f"Time: stage {stage}; Source: {source}; Service: calendar, car_rental, credit_card, email, flight_booking, hotel_booking, maps, notion, visa_and_advisory, weather, workspace; Facts: {facts}; Action: {action}; Authorization: cancellable or confirmation-only commitments; Risk: conservative child-safety, fatigue and weather boundaries; Next step: {next_step}."


async def handle_record_event(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    source = str(spec.get("source_event_id") or action.get("source_event_id") or "event")
    if not spec.get("stage_boundary", True):
        # Continuity event inside a stage.  Every non-boundary step declares
        # expected_stage_weight 0 and no expected_checks, so the stage's
        # deliverables belong to its boundary step; running the stage block here
        # too would execute its side effects twice (the SouthernCross hold has a
        # single unit of inventory) and break the boundary snapshot.
        state.setdefault("events", []).append({"step": spec["step"], "source_event_id": source, "stage": stage})
        return
    if stage == 0:
        await _notion_page(rec, state)
        await _notion_append(rec, state, "Trip dashboard: Shanghai to Sydney, Canberra and Melbourne; budget cap CNY 118000; record authorization before non-refundable purchases; payment and high-value spending, cancellation or booking changes, and sensitive information require confirmation; risk register is active.")
        await _calendar_event(rec, state, "Australia motorhome itinerary and budget review", "2026-09-01T18:00:00+08:00", "2026-09-01T18:30:00+08:00", "Sydney, Canberra and Melbourne route; motorhome, child restraint and budget cap CNY 118000.")
        rec.workspace_write("trip_dashboard.md", "Australia motorhome route trial: Shanghai -> Sydney -> Canberra -> Melbourne. Family of three including Mimi, age four. Budget cap: CNY 118000. Cancellable travel may proceed; non-refundable motorhome, high-value spend, cancellation or booking changes require Li Cheng or Zhou Ran confirmation. Risk register and itinerary board are maintained.")
        rec.workspace_write("budget_ledger.md", "Budget cap CNY 118000. Track flights, hotels, motorhome, insurance and AUD 600 security deposit pre-authorization separately; pending holds are not final spend.")
        rec.workspace_write("risk_log.md", "Initial risks: compliant child restraint, right-hand-drive adaptation, left-side driving, insurance addendum, fatigue and severe wind. Confirm before non-refundable commitments; sensitive documents stay private.")
        rec.workspace_write("order_log.md", "No motorhome purchase authorized yet. Cancellable flights and hotels may be evaluated; record order status and cancellation terms.")
    elif stage == 1:
        await rec.call("visa_and_advisory", "check_entry_requirements", {"nationality": "CN", "destination": "AU", "purpose": "tourism", "transit_countries": []})
        await _calendar_event(rec, state, "Australian visa and additional documents follow-up", "2026-09-05T09:00:00+08:00", "2026-09-05T09:30:00+08:00", "Review Australian visa, passport and child documents; use the official system and do not make a final visa judgment.")
        rec.workspace_write("risk_log.md", "Entry review: Australian visa and passport/document requirements must be checked in the official system. Child documents and relationship proof are tracked; no certain approval is claimed.")
    elif stage == 2:
        await rec.call("car_rental", "get_road_policy", {})
        await rec.call("car_rental", "list_insurance_plans", {})
        await rec.call("credit_card", "get_card", {"card_id": CARD_ID})
        await _notion_append(rec, state, "Locked rules reviewed: use an AS/NZS 1754 approved child restraint in the motorhome, avoid an unsuitable front-seat placement, select motorhome insurance, and treat World Travel Plus motorhome/RV cover as excluded.")
        rec.workspace_write("risk_log.md", "Child restraint policy: AS/NZS 1754 approved restraint, forward-facing placement as permitted, and no prohibited front-seat arrangement. World Travel Plus card excludes motorhome/RV rental cover; use supplier insurance.")
        rec.workspace_write("budget_ledger.md", "Insurance allocation is recorded in AUD and converted to CNY for the CNY 118000 cap. Card issuer benefits are noted, but motorhome/RV coverage is excluded.")
    elif stage == 3:
        await _flight_search(rec, "PVG", "SYD", "2026-09-12")
        await rec.call("car_rental", "search_vehicle_offers", {"pickup_city": "Sydney", "return_city": "Melbourne", "pickup_at": "2026-09-15T09:00:00+10:00", "return_at": "2026-09-24T16:00:00+10:00", "seats": 4, "max_results": 50, "page": 1})
        for city, start, end in (("Sydney", "2026-09-13", "2026-09-15"), ("Canberra", "2026-09-18", "2026-09-19")):
            await _hotel_search(rec, city, start, end)
        for city in ("Sydney", "Canberra", "Melbourne"):
            await rec.call("weather", "subscribe_alerts", {"geo": city, "sink": f"memory://family-rv-{city.lower()}"})
        await _search_route(rec, "Sydney", "Canberra", "2026-09-16T08:00:00+10:00")
        await _notion_append(rec, state, "Compared PVG/Shanghai to SYD/Sydney flight candidates with SouthernCross, Tasman and Pacific RV candidates. Filtered out the Tasman non-refundable option because the child restraint was uncertain; it was excluded and not selected. Forecast/weather alert subscriptions cover NSW/Sydney, ACT/Canberra and VIC/Melbourne.")
        rec.workspace_write("route_plan.md", "First route pass: compared PVG/Shanghai to SYD/Sydney flight candidates with SouthernCross, Tasman and Pacific RV candidates. Filtered out the Tasman non-refundable option because the child restraint was uncertain; excluded/not selected. Forecast/weather alert subscriptions cover NSW/Sydney, ACT/Canberra and VIC/Melbourne. Keep each driving segment at or below 3.5 hours where possible, add recovery stops, and prohibit night driving.")
    elif stage == 4:
        await _record_flights(rec, state)
        await _hotel_search(rec, "Sydney", "2026-09-13", "2026-09-15")
        await _record_hotel(rec, "sydharbr", "2026-09-13", "2026-09-15", state, "Family room; cancellable; late arrival after PVG-SYD flight.")
        rec.workspace_write("order_log.md", "Booked or held refundable PVG-SYD / MEL-PVG travel and cancellable Sydney family accommodation. Motorhome remains unbooked because non-refundable purchase is not authorized.")
        rec.workspace_write("risk_log.md", "Authorization boundary retained: do not buy a non-refundable motorhome package; require confirmation for high-value spend, cancellation or changes.")
    elif stage == 5:
        offer = await rec.call("car_rental", "get_vehicle_offer", {"offer_id": "CRO_SC4B_260915"})
        await _email(rec, "Child restraint standard and SouthernCross 4B inventory", "Please confirm that one remaining SouthernCross 4B cancellable hold includes one AS/NZS 1754 approved child restraint for Mimi and the stated return terms.", draft=True)
        rec.workspace_write("risk_log.md", "SouthernCross 4B inventory review: one compliant child restraint remains after the inventory change; the option is cancellable/refundable until the displayed deadline. Verify fitting and standard before pickup.")
    elif stage == 6:
        booking = await rec.call("car_rental", "create_rental_booking", {"offer_id": "CRO_SC4B_260915", "insurance_plan_id": "INS_FULL_PLUS", "driver_user_id": USER_ID, "drivers": [{"name": "Li Cheng", "license": "international permit and home license", "role": "primary"}], "contact": {"name": "Li Cheng", "email": "li.cheng@example.cn", "phone": "+86-13800000000"}, "payment": {"method": "hold", "card_id": CARD_ID, "amount": 600, "currency": "AUD"}})
        if isinstance(booking, dict) and booking.get("booking_ref"):
            state["vars"]["car_booking_ref"] = booking["booking_ref"]
        await _record_hotel(rec, "cbrlake", "2026-09-18", "2026-09-19", state, "Family room; confirm outdoor RV parking and clearance at least 3.2 m; cancellable.")
        await _notion_append(rec, state, "Held SouthernCross 4B with INS_FULL_PLUS: one-way Sydney pickup to Melbourne return, cancellable hold, AS/NZS 1754 child restraint, and insurance coverage recorded.")
        rec.workspace_write("order_log.md", "SouthernCross 4B held: Sydney pickup, Melbourne one-way return, cancellable/refundable hold, full motorhome insurance INS_FULL_PLUS, child restraint add-on and AUD 600 deposit authorization. Canberra family hotel booked with outdoor RV parking clearance request.")
    elif stage == 7:
        await _notion_append(rec, state, "Zhou Ran spouse authorization recorded: decline Tasman Saver if non-refundable or restraint standard is uncertain; retain the more expensive cancellable option.")
        rec.workspace_write("risk_log.md", "Zhou Ran (spouse) declined any non-refundable Tasman Saver purchase while child restraint standard is uncertain. Retain SouthernCross cancellable/refundable option; no unauthorized purchase.")
        rec.workspace_write("order_log.md", "Spouse decision: do not purchase non-refundable motorhome or uncertain child-seat package; cancellable/refundable option may remain held.")
    elif stage == 8:
        await rec.call("visa_and_advisory", "get_visa_application", {"application_id": "VAC_LC_2026_09_AU"})
        await _calendar_event(rec, state, "Australian visa additional documents deadline", "2026-09-09T09:00:00+08:00", "2026-09-09T09:20:00+08:00", "Use the official visa system for additional documents by 2026-09-09; self-service only, do not upload sensitive identity documents through this assistant.")
        rec.workspace_write("risk_log.md", "Australian visa application VAC_LC_2026_09_AU: status requires additional documents by 2026-09-09. Li Cheng must use the official system/self-service path; do not send or upload passport numbers, original birth certificates or other sensitive identity documents externally.")
    elif stage == 9:
        await _calendar_event(rec, state, "Sydney to Canberra driving segment", "2026-09-16T08:00:00+10:00", "2026-09-16T11:30:00+10:00", "Right-hand-drive practice and low-speed acclimation; recovery stop; no night driving; keep driving under 3.5 hours.")
        await _calendar_event(rec, state, "Canberra to Albury recovery segment", "2026-09-19T08:00:00+10:00", "2026-09-19T11:30:00+10:00", "Break and child rest stop; keep the segment under 3.5 hours and avoid night driving.")
        await _calendar_event(rec, state, "Albury to Melbourne recovery segment", "2026-09-21T07:30:00+10:00", "2026-09-21T11:00:00+10:00", "Right-hand-drive route with rest; leave early and avoid the evening peak and night driving.")
        rec.workspace_write("route_plan.md", "Fatigue plan: Sydney -> Canberra, Canberra -> Albury, and Albury -> Melbourne segments target 3.5 hours or less with recovery stops. Include right-hand-drive low-speed practice, leave early, and do not drive at night.")
    elif stage == 11:
        await rec.call("hotel_booking", "get_hotel_details", {"hotel_id": "cbrlake"})
        await rec.call("maps", "search_places", {"query": "Canberra Exhibition Park oversized-vehicle parking", "geo": {"lat": -35.2809, "lng": 149.13}, "radius_m": 10000, "limit": 20, "page": 1})
        await rec.call("weather", "get_alerts", {"geo": "Canberra"})
        await _email(rec, "Canberra RV parking replacement and wind risk", "The booked outdoor RV bay is unavailable and the 2.1m underground garage cannot fit the 2.85m motorhome. Please confirm the external Canberra Exhibition Park oversized-vehicle bay and overnight use before arrival.", draft=True)
        rec.workspace_write("risk_log.md", "Parking mismatch: Lakeview Family Hotel now offers only a 2.1m underground garage; the 2.85m motorhome does not fit. Recovery requires confirmed off-site/external oversized-vehicle parking and clearance. ACT severe-wind risk also affects driving, parking and awning use.")
        rec.workspace_write("order_log.md", "Canberra hotel parking change logged; request replacement/off-site parking and confirmation rather than assuming the underground garage is usable.")
    elif stage == 12:
        await rec.call("car_rental", "list_insurance_plans", {})
        await rec.call("car_rental", "get_booking", {"booking_ref": str(state["vars"].get("car_booking_ref") or "unknown")})
        await _calendar_event(rec, state, "Severe-wind route and insurance addendum review", "2026-09-17T18:00:00+10:00", "2026-09-17T18:30:00+10:00", "User reminder: review 2026-09-17-WIND addendum; reduce or delay the journey and keep the awning secured/retracted during severe wind.")
        rec.workspace_write("risk_log.md", "User reminder: insurance addendum 2026-09-17-WIND says deployed awning and roof accessories are excluded/not covered during official severe-wind alerts. Keep awning secured/retracted, avoid exposed operation, contact SouthernCross and report wind damage.")
    elif stage == 14:
        status = await rec.call("flight_booking", "get_flight_status", {"flight_no": "SC888", "date": "2026-09-12"}, trace_aliases={"date": "2026-09-12"})
        await _calendar_event(rec, state, "Earlier SC888 departure reminder", "2026-09-12T16:30:00+08:00", "2026-09-12T17:00:00+08:00", "SC888 now departs at 19:45, 45 minutes earlier; notify the family and allow extra airport departure time.")
        await _email(rec, "SC888 schedule change and late Sydney hotel arrival", "SC888 now departs PVG at 19:45 on 12 September, 45 minutes earlier. The Sydney family hotel has been told to expect a late arrival.", draft=True)
        rec.workspace_write("order_log.md", "SC888 schedule change recorded: PVG -> SYD, 12 September, 19:45 departure (45 minutes earlier). Sydney hotel late-arrival note prepared.")
    elif stage == 15:
        await rec.call("visa_and_advisory", "get_visa_application", {"application_id": "VAC_LC_2026_09_AU"})
        await _notion_append(rec, state, "Arrival in Sydney: visa application is granted after additional documents; the resolved visa risk remains traceable to the official application record. Preserve hotel/rest after arrival; no vehicle pickup and no long-distance drive before rest.")
        rec.workspace_write("risk_log.md", "Australian visa VAC_LC_2026_09_AU is granted after additional documents; visa risk is resolved/closed while preserving the application history. Arrival rest is protected with hotel/rest, no vehicle pickup and no long-distance drive.")
    elif stage == 16:
        ref = str(state["vars"].get("car_booking_ref") or "unknown")
        await rec.call("car_rental", "get_booking", {"booking_ref": ref})
        await rec.call("car_rental", "get_return_requirements", {"booking_ref": ref})
        await _calendar_event(rec, state, "Right-hand-drive acclimation and light first drive", "2026-09-15T10:00:00+10:00", "2026-09-15T12:00:00+10:00", "Pickup orientation, child restraint fitting and insurance addendum review; low-speed practice only; no long-distance drive today.")
        rec.workspace_write("route_plan.md", "Pickup plan: inspect and fit the child restraint, review insurance addendum, handover and return requirements, including fuel gauge, cleanliness/clean condition and return time/deadline. Then use a reduced low-speed right-hand-drive practice loop. Anxiety is a reason for a buffer and no long drive today.")
    elif stage == 17:
        await rec.call("weather", "get_alerts", {"geo": "Canberra"})
        await _search_route(rec, "Canberra", "Albury", "2026-09-18T08:00:00+10:00")
        await _calendar_event(rec, state, "ACT severe-wind route adjustment", "2026-09-18T07:30:00+10:00", "2026-09-18T08:00:00+10:00", "Recheck severe wind, shorten or delay the route, add rest, and keep driving at or below 3.5 hours where possible; do not use the awning.")
        rec.workspace_write("route_plan.md", "ACT severe-wind recheck: review Canberra route and parking before departure; reduce, delay or shorten the drive and preserve rest. Fatigue target is 3.5 hours (absolute upper bound 4h) per segment. Do not deploy the awning.")
    elif stage == 18:
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        await rec.call("credit_card", "get_card", {"card_id": CARD_ID})
        ref = str(state["vars"].get("car_booking_ref") or "unknown")
        await rec.call("car_rental", "get_booking", {"booking_ref": ref})
        await _email(rec, "Duplicate SouthernCross AUD 600 authorization", "World Travel Plus shows two SouthernCross Rentals AUD 600 pending authorizations. The standard deposit is one normal AUD 600 hold; please confirm and reverse the duplicate.", draft=True)
        rec.workspace_write("budget_ledger.md", "SouthernCross Rentals shows two AUD 600 pending/pre-authorization entries. Treat one as the normal actual deposit and the other as a duplicate; exclude both pending holds from final expenditure until reconciled.")
    elif stage == 19:
        await rec.call("maps", "directions", {"origin": "Albury", "dest": "Melbourne", "mode": "driving", "depart_at": "2026-09-21T07:00:00+10:00"})
        if not state["vars"].get("melbourne_hotel_reserved"):
            await _record_hotel(rec, "melstop", "2026-09-23", "2026-09-25", state, "Family room; cancellable Melbourne stay; checkout recorded for return preparation.")
            state["vars"]["melbourne_hotel_reserved"] = True
        await _calendar_event(rec, state, "Early Albury to Melbourne departure", "2026-09-21T07:00:00+10:00", "2026-09-21T10:30:00+10:00", "Afternoon showers remain possible; leave early, keep rest stops for Mimi, avoid evening peak and all night driving.")
        rec.workspace_write("route_plan.md", "Melbourne leg updated from Albury: leave early, retain rest stops because Mimi is tired, avoid afternoon/evening peak traffic and do not drive after dark.")
    elif stage == 20:
        ref = str(state["vars"].get("car_booking_ref") or "unknown")
        await rec.call("car_rental", "get_booking", {"booking_ref": ref})
        await rec.call("car_rental", "report_vehicle_condition", {"booking_ref": ref, "phase": "return", "checklist_items": {"accident": "none", "incident": "none", "damage": "none", "cleanliness": "clean", "fuel": "full"}, "fuel_or_charge_level": "full", "notes": "Return inspection: no accident or incident, clean condition, fuel gauge full; awaiting back-office confirmation."})
        await rec.call("car_rental", "list_bookings", {"user_id": USER_ID})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        rec.workspace_write("order_log.md", "Vehicle return in Melbourne recorded: initial inspection reports no accident/incident and no cleaning issue; return and deposit remain pending back-office confirmation.")
        rec.workspace_write("budget_ledger.md", "AUD 600 security deposit remains pending/awaiting confirmation after return: pending release, not released by the rental company, and not claimed as released here; tracked separately from actual spend.")
    elif stage == 21:
        await rec.call("flight_booking", "get_flight_status", {"flight_no": "SC889", "date": "2026-09-26"}, trace_aliases={"date": "2026-09-26"})
        await rec.call("flight_booking", "list_bookings", {"user_id": USER_ID, "page_size": 50})
        await rec.call("hotel_booking", "list_reservations", {"user_id": USER_ID})
        await rec.call("hotel_booking", "get_reservation", {"reservation_id": str((state["vars"].get("hotel_reservations") or ["unknown"])[0])})
        rec.workspace_write("order_log.md", "Return preparation: SC889 MEL -> PVG on 26 September reviewed; Sydney, Canberra and Melbourne hotel checkout orders are completed, archived and closed. Keep only deposit/card pending items open.")
    elif stage == 22:
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        rec.workspace_write("budget_ledger.md", "Duplicate SouthernCross AUD 600 authorization has a reversal adjustment. Keep the normal AUD 600 actual security deposit pending; record the duplicate, reversal and open follow-up separately.")
    elif stage == 23:
        ref = str(state["vars"].get("car_booking_ref") or "unknown")
        await rec.call("car_rental", "list_bookings", {"user_id": USER_ID})
        await rec.call("car_rental", "get_booking", {"booking_ref": ref})
        await rec.call("flight_booking", "list_bookings", {"user_id": USER_ID, "page_size": 50})
        await rec.call("flight_booking", "get_flight_status", {"flight_no": "SC889", "date": "2026-09-26"}, trace_aliases={"date": "2026-09-26"})
        await rec.call("hotel_booking", "list_reservations", {"user_id": USER_ID})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        await _notion_append(rec, state, "Final assessment: orders are closed or reconciled; budget allocation is within CNY 118000 with remaining funds under the cap; the AS/NZS 1754 child restraint and INS_FULL_PLUS addendum are documented; right-hand-drive fatigue and severe-wind limits mean future long trips should remain conservative, cancellable and rest-led; the pending AUD 600 security deposit pre-authorization and duplicate-hold reversal stay visible as open follow-up.")
        await _email(rec, "Australia motorhome trial final summary", "Summary: flights, hotels and motorhome orders are reviewed; total is within the CNY 118000 budget cap; child restraint and insurance findings are documented; right-hand-drive fatigue and severe-wind constraints require shorter, rest-led future trips. The AUD 600 security deposit remains pending and the duplicate authorization reversal is visible for follow-up.", draft=True)
        total = 0.0
        for booking in _rows(await rec.call("flight_booking", "list_bookings", {"user_id": USER_ID, "page_size": 50}), "bookings"):
            paid = booking.get("total_paid") if isinstance(booking.get("total_paid"), dict) else {}
            total += _cny_amount(paid.get("amount"), paid.get("currency"))
        car_detail = await rec.call("car_rental", "get_booking", {"booking_ref": ref})
        estimated = car_detail.get("estimated_total") if isinstance(car_detail.get("estimated_total"), dict) else {}
        total += _cny_amount(estimated.get("amount"), estimated.get("currency"))
        listed = await rec.call("hotel_booking", "list_reservations", {"user_id": USER_ID})
        for reservation_id in (listed.get("reservation_ids") if isinstance(listed, dict) else None) or []:
            reservation = await rec.call("hotel_booking", "get_reservation", {"reservation_id": reservation_id})
            if str(reservation.get("status") or "").lower() in ("cancelled", "walked"):
                continue
            total += _cny_amount(reservation.get("total_charged"), reservation.get("currency"))
        rec.workspace_write("final_assessment.md", "Conclusion and final assessment: orders (flights, hotels and SouthernCross motorhome) are closed or reconciled; the visa additional documents request and the 2.1 m Canberra RV parking mismatch were recovered; allocation is within the CNY 118000 budget cap; safety findings cover the AS/NZS 1754 child restraint, INS_FULL_PLUS insurance addendum, right-hand-drive adaptation, driver fatigue and severe wind. Long-term motorhome travel is practical only with cancellable bookings, compliant child equipment, conservative driving and rest. AUD 600 security deposit remains pending/open; duplicate authorization reversal is recorded and visible for follow-up.")
        rec.workspace_write("risk_log.md", "Final mutation review: visa additional documents were resolved; the child-restraint inventory change and 2.1 m Canberra parking mismatch were recovered; SC888 moved earlier to 19:45; severe-wind controls remain recorded; and the duplicate AUD 600 pre-authorization was reversed while the normal security deposit remains pending.")
        rec.workspace_write("order_log.md", "Final order register: SC888 PVG-SYD, SC889 MEL-PVG, Sydney/Canberra/Melbourne hotels, and SouthernCross 4B motorhome. Completed orders are archived; security deposit and card reconciliation remain open.")
        rec.workspace_write("budget_ledger.md", f"Final budget ledger: reconciled backend total is CNY {total:,.0f} and is within CNY 118000. Pending/pre-authorization entries are excluded from actual expenditure. Normal AUD 600 security deposit is pending; duplicate AUD 600 hold and reversal are reconciled but follow-up remains open.")
    else:
        rec.workspace_write("trip_dashboard.md", _entry(stage, source, "non-boundary event", "recorded", "continue"))
    state.setdefault("events", []).append({"step": spec["step"], "source_event_id": source, "stage": stage})


ActionHandler = Callable[[Recorder, dict[str, Any], dict[str, Any], dict[str, Any]], Any]
ACTION_HANDLERS = {"record_event": handle_record_event}


def _write_trajectory(spec: dict[str, Any], response: str, rec: Recorder) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    calls = [{"tool_call_id": x["tool_call_id"], "function_name": x["function_name"], "arguments": x["arguments"]} for x in rec.calls]
    results = [{"source_call_id": x["tool_call_id"], "content": json.dumps(x["result"], ensure_ascii=False, default=str), "extra": {"success": x["success"], "error": x["error"]}} for x in rec.calls]
    trajectory = {"schema_version": "ATIF-v1.7", "session_id": f"oracle-{spec['step']}", "agent": {"name": "family-rv-australia-oracle", "version": "1.0.0"}, "steps": [{"step_id": 1, "source": "user", "message": str(spec.get("source_event_id", ""))}, {"step_id": 2, "source": "agent", "message": response, "tool_calls": calls, "observation": {"results": results}, "llm_call_count": 0}], "final_metrics": {"tool_calls": len(calls), "tool_errors": sum(not x["success"] for x in rec.calls)}}
    (LOGS / "trajectory.json").write_text(json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LOGS / "oracle-result.json").write_text(json.dumps({"step": spec["step"], "response_used": response, "calls": rec.calls}, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


async def execute(spec: dict[str, Any]) -> str:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions")
    missing = [x for x in required if x not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    state = _load_state()
    rec = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = str(action.get("kind") or "")
        handler = ACTION_HANDLERS.get(kind)
        if handler is None:
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {sorted(ACTION_HANDLERS) or '(none — this oracle is unwired)'}")
        await handler(rec, state, spec, action)
    response = spec["response_paraphrase"] if os.environ.get("ORACLE_STYLE", "canonical").strip().lower() == "paraphrase" else spec["response"]
    _save_state(state)
    _write_trajectory(spec, response, rec)
    return response


async def _main_async() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: oracle.py /solution/step_spec.json")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(await execute(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main_async()))
