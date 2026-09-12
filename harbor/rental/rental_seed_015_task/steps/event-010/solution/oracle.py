#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "rental_seed_015_task"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "I maintained the rental evidence chain with verified routes, privacy boundaries, and confirmation-aware next steps."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "email": "http://email:8000/mcp",
    "listing_platform": "http://listing-platform:8000/mcp",
    "maps": "http://maps:8000/mcp",
    "notification_hub": "http://notification-hub:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "review_platform": "http://review-platform:8000/mcp",
}
USER_ID = "usr_liyan"
CALENDAR_ID = "cal_liyan_main"
NOTION_PAGE_ID = "pg_liyan_family_housing"

ROUTE_IDS = {
    "Clear Bay Garden": "place_a",
    "Mingcheng Court": "place_b",
    "Hexi Qingyuan": "place_c",
    "Yunanli": "place_d",
    "South Creek Garden": "place_e",
    "Clearwave Residence": "place_h",
    "Mingcheng Road Primary School": "place_school",
    "Hexi South Digital Services Center": "place_company",
    "Clear Bay Fresh Select": "poi_chengwan_fresh",
    "Yunanli Community Market": "poi_yunanli_fresh",
    "South Creek Neighborhood Market": "poi_nanxiyuan_market",
    "Clearwave Neighborhood Fresh Market": "poi_h_market",
    "Jiangdong South Road detour transfer point": "place_b_detour_junction",
}

# Route tools accept place ids directly, but exact localized names exercise the
# same geocoder surface available to the agent.  Keep ids separate for result
# validation instead of appending them to the free-form query.
ROUTE_VALUES = {
    "Clear Bay Garden": "\u6f84\u6e7e\u82b1\u56ed",
    "Mingcheng Court": "\u660e\u6f84\u96c5\u82d1",
    "Hexi Qingyuan": "\u6cb3\u897f\u6674\u56ed",
    "Yunanli": "\u4e91\u5cb8\u91cc",
    "South Creek Garden": "\u5357\u6eaa\u82d1",
    "Clearwave Residence": "\u6e05\u6f9c\u516c\u9986",
    "Mingcheng Road Primary School": "\u660e\u6f84\u8def\u5c0f\u5b66",
    "Hexi South Digital Services Center": "\u6cb3\u897f\u5357\u6570\u5b57\u670d\u52a1\u4e2d\u5fc3",
    "Clear Bay Fresh Select": "\u6f84\u6e7e\u9c9c\u9009",
    "Yunanli Community Market": "\u4e91\u5cb8\u91cc\u793e\u533a\u83dc\u573a",
    "South Creek Neighborhood Market": "\u5357\u6eaa\u82d1\u90bb\u91cc\u8d85\u5e02",
    "Clearwave Neighborhood Fresh Market": "\u6e05\u6f9c\u90bb\u91cc\u751f\u9c9c",
    "Jiangdong South Road detour transfer point": "\u6c5f\u4e1c\u5357\u8def\u7ed5\u884c\u63a5\u9a73\u70b9",
}


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
    """Normalize MCP return shapes, including successful empty reads."""
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
    """Fail closed on explicit error envelopes while accepting empty reads."""
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
    """Call MCP services and retain exact ATIF evidence for this turn."""

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
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": value, "success": True, "error": None})
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": {"error": error}, "success": False, "error": error})
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


def _save_state(state: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    temp = STATE_PATH.with_suffix(STATE_PATH.suffix + ".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(STATE_PATH)


def _rich(text: str) -> dict[str, Any]:
    return {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


async def _notion(rec: Recorder, text: str) -> None:
    await rec.call("notion", "API-patch-block-children", {"block_id": NOTION_PAGE_ID, "children": [_rich(text)]})


async def _list_calendar(rec: Recorder) -> None:
    await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 500})


async def _route(rec: Recorder, origin: str, dest: str, at: str) -> None:
    for label in (origin, dest):
        if label not in ROUTE_IDS:
            continue
        geocode = await rec.call("maps", "geocode", {"address": ROUTE_VALUES[label]})
        if not isinstance(geocode, dict) or geocode.get("place_id") != ROUTE_IDS[label]:
            raise RuntimeError(f"maps.geocode resolved the wrong place for {label!r}: {geocode!r}")
    result = await rec.call("maps", "get_traffic_estimate", {"origin": ROUTE_VALUES.get(origin, origin), "dest": ROUTE_VALUES.get(dest, dest), "depart_at": at})
    if not isinstance(result, dict) or not isinstance(result.get("with_traffic_duration_s"), int):
        raise RuntimeError(f"maps.get_traffic_estimate returned no usable route: {result!r}")


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in keys:
            rows = value.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


async def _search_listings(rec: Recorder, expected_ids: tuple[str, ...], **arguments: Any) -> None:
    result = await rec.call("listing_platform", "search_listings", arguments)
    found = {str(row.get("listing_id") or "") for row in _rows(result, "items", "results", "listings")}
    missing = set(expected_ids) - found
    if missing:
        raise RuntimeError(f"listing search omitted expected ids: {sorted(missing)!r}")


async def _morning(rec: Recorder, day: str, homes: tuple[str, ...]) -> None:
    for home in homes:
        await _route(rec, home, "Mingcheng Road Primary School", f"{day}T07:20:00+08:00")
    await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", f"{day}T07:55:00+08:00")


async def _handle_record_event(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    vars = state["vars"]
    completed = vars.setdefault("completed_stages", [])
    if not isinstance(completed, list):
        raise RuntimeError("oracle completed_stages state must be a list")
    if stage in completed:
        return
    if not bool(spec.get("stage_boundary", action.get("stage_boundary", False))):
        state["events"].append({"step": spec.get("step"), "stage": stage, "deferred": True})
        return
    if stage == 0:
        await _search_listings(rec, ("listing_d",), category="rent", city="\u5357\u4eac", max_price_minor=750000, min_rooms=2, max_rooms=2, limit=100)
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_d"})
        await _list_calendar(rec)
        await _notion(rec, "Family rental control desk: Nanjing whole-unit rental, two-bedroom unit, monthly rent ceiling CNY 7,500, move-in before the 2026-08-08 lease expiration, morning transportation chain with an 8-minute school drop-off stop and a 75-minute cap, aftercare to 18:00, fresh-food supermarket walking target 15 minutes, and elevator evidence are tracked. Candidate tracker, route matrix, budget ledger, risk register, authorization log, privacy materials register, and next-step evidence are maintained. Query and draft work can be handled directly; query and draft actions can handle directly, while any appointment, viewing, external sending, payment, holding fee, contract signing, or child documents require confirmation each time; confirm each time, keep the privacy boundary, and school-district eligibility remains unverified.")
    elif stage == 1:
        await _search_listings(rec, ("listing_c", "listing_f", "listing_g"), category="rent", city="\u5357\u4eac", district="\u5efa\u90ba\u533a", min_rooms=1, max_rooms=2, sort="price_asc", limit=100)
        for lid in ("listing_c", "listing_f", "listing_g"):
            await rec.call("listing_platform", "get_listing_detail", {"listing_id": lid})
        await _notion(rec, "Hard filter matrix: Hexi Qingyuan listing_c is over the CNY 7,500 budget at 7,600, Old Street Academy listing_f is a high-floor two-bedroom with no elevator, and Linjiang New Residence listing_g is a one-bedroom. These remain visible as rejected or history; no unsupported school-district claim is accepted.")
    elif stage == 2:
        await _list_calendar(rec)
        await rec.call("notification_hub", "list_subscriptions", {"user_id": USER_ID})
        if not vars.get("review_event"):
            await rec.call("calendar", "update_event", {"event_id": "evt_client_weekly_review", "calendar_id": CALENDAR_ID, "description": "Weekly work review remains scheduled; perform a 72-hour candidate listing, route, elevator, fee, and calendar review."})
            vars["review_event"] = True
        await _notion(rec, "Calendar baseline recorded: work hours 09:30-17:30, Mingcheng Road Primary School aftercare to 18:00, parent meeting, and lease expiration on 2026-08-08. A recurring 72-hour review covers listing status, route evidence, elevator status, fees, viewing windows, documents, and calendar conflicts.")
    elif stage == 3:
        await _search_listings(rec, ("listing_a", "listing_b", "listing_c", "listing_d", "listing_e"), category="rent", city="\u5357\u4eac", max_price_minor=760000, min_rooms=2, max_rooms=2, sort="newest", limit=100)
        for lid in ("listing_a", "listing_b", "listing_c", "listing_d", "listing_e"):
            await rec.call("listing_platform", "get_listing_detail", {"listing_id": lid})
        await _notion(rec, "Budget ledger refresh: Clear Bay Garden listing_a, Mingcheng Court listing_b, Yunanli listing_d, and South Creek Garden listing_e remain active two-bedroom candidates at or below CNY 7,500. Hexi Qingyuan listing_c is retained as over budget history at CNY 7600 and eliminated from the current shortlist; one-time deposit, holding fee, and other charges are separate from monthly rent.")
    elif stage == 4:
        await _morning(rec, "2026-07-10", ("Clear Bay Garden", "Mingcheng Court", "Hexi Qingyuan", "Yunanli", "South Creek Garden"))
        for home, market in (("Clear Bay Garden", "Clear Bay Fresh Select"), ("Yunanli", "Yunanli Community Market"), ("South Creek Garden", "South Creek Neighborhood Market")):
            await rec.call("maps", "directions", {"origin": ROUTE_VALUES[home], "dest": ROUTE_VALUES[market], "mode": "walking", "depart_at": "2026-07-10T18:00:00+08:00"})
        for market in ("Clear Bay Fresh Select", "Yunanli Community Market", "South Creek Neighborhood Market"):
            places = await rec.call("maps", "search_places", {"query": ROUTE_VALUES[market], "limit": 20})
            place_ids = {str(row.get("place_id") or "") for row in _rows(places, "items", "results")}
            if ROUTE_IDS[market] not in place_ids:
                raise RuntimeError(f"maps.search_places omitted required market {market!r}")
        await _notion(rec, "Initial route matrix: Clear Bay Garden, Mingcheng Court, Yunanli, and South Creek Garden have the morning home-school-office chain within the 75-minute target after the 8-minute school drop-off stop; Hexi Qingyuan exceeds the route cap. The school-to-office leg is explicit. Fresh-food supermarket walking routes use the usable entrance and remain within the 15-minute target for the viable comparison set.")
    elif stage == 5:
        await _list_calendar(rec)
        await _notion(rec, "Care coverage record: the sister is a date-specific backup for specified dates only, not ongoing, and not assumed. Regular school aftercare remains until 18:00; family assistance is used only on explicitly confirmed dates and does not replace the long-term transportation chain.")
    elif stage == 6:
        for merchant in ("mer_a", "mer_b", "mer_e"):
            await rec.call("review_platform", "list_reviews", {"merchant_id": merchant, "limit": 50})
        await _list_calendar(rec)
        await _notion(rec, "Review evidence checked for Clear Bay Garden elevator availability, Mingcheng Court morning rush hour and school-district marketing risk, and South Creek Garden fees requiring written confirmation. Clear Bay Garden, Mingcheng Court, and South Creek Garden viewing windows are proposed only and remain pending user confirmation; no external appointment, payment, or contract action was taken.")
    elif stage == 7:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_a"})
        await rec.call("review_platform", "list_reviews", {"merchant_id": "mer_a", "limit": 50})
        await _notion(rec, "Clear Bay Garden listing_a elevator maintenance is recorded for 2026-07-18 through 2026-07-29. The high-floor candidate is downgraded as not suitable for move-in during the maintenance window until stable operation is reverified.")
    elif stage == 8:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_a"})
        await rec.call("review_platform", "list_reviews", {"merchant_id": "mer_a", "limit": 50})
        await _list_calendar(rec)
        await _notion(rec, "The 72-hour refresh propagated Clear Bay Garden elevator maintenance and the related resident review into the candidate tracker and risk register; listing_a remains downgraded and no payment, contract, or viewing commitment was created.")
    elif stage == 9:
        message = "Please confirm the elevator's current operating status, the deposit and any child-damage deposit, whether a child may live in the unit, and available viewing windows. This is a text question only; no child documents or school documents are attached, and school-district marketing is unverified."
        await rec.call("listing_platform", "contact_agent", {"user_id": USER_ID, "listing_id": "listing_b", "message": message})
        await rec.call("listing_platform", "contact_agent", {"user_id": USER_ID, "listing_id": "listing_e", "message": message})
        await rec.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await _notion(rec, "Authorized text questions were sent only to Mingcheng Court listing_b and South Creek Garden listing_e, limited to elevator, deposit, child occupancy, and viewing window. No attachment was sent; school-district guarantee language is logged as unverified marketing and not treated as a conclusion.")
    elif stage == 10:
        await rec.call("maps", "get_place_details", {"place_id": "place_b"})
        await rec.call("maps", "get_place_details", {"place_id": "place_b_detour_junction"})
        await _route(rec, "Mingcheng Court", "Jiangdong South Road detour transfer point", "2026-07-17T07:20:00+08:00")
        await _route(rec, "Jiangdong South Road detour transfer point", "Mingcheng Road Primary School", "2026-07-17T07:35:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-17T08:00:00+08:00")
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_route_b_traffic"})
        await _notion(rec, "Mingcheng Court listing_b route refresh: the Jiangdong South Road detour transfer point and one-way restriction are now part of the morning transportation chain. The 83-minute result is recorded. The three route segments, 8-minute school drop-off stop, and school-to-office leg are recomputed; the old route cache is not reused.")
    elif stage == 11:
        await rec.call("maps", "get_place_details", {"place_id": "place_b"})
        await _route(rec, "Mingcheng Court", "Jiangdong South Road detour transfer point", "2026-07-17T07:20:00+08:00")
        await _route(rec, "Jiangdong South Road detour transfer point", "Mingcheng Road Primary School", "2026-07-17T07:35:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-17T08:00:00+08:00")
        await _notion(rec, "Traffic mutation rechecked: Mingcheng Court's cached morning route is invalidated and replaced by the detour evidence. The resulting 83-minute chain exceeds the 75-minute hard requirement, so listing_b is eliminated for this transportation constraint despite its rent and elevator status.")
    elif stage == 12:
        for lid in ("listing_d", "listing_e", "listing_b"):
            await rec.call("listing_platform", "get_listing_detail", {"listing_id": lid})
        await _morning(rec, "2026-07-18", ("Yunanli", "South Creek Garden"))
        await _route(rec, "Mingcheng Court", "Jiangdong South Road detour transfer point", "2026-07-17T07:20:00+08:00")
        await _route(rec, "Jiangdong South Road detour transfer point", "Mingcheng Road Primary School", "2026-07-17T07:35:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-17T08:00:00+08:00")
        await _notion(rec, "Shortlist ranking: Yunanli listing_d is the transportation backup, South Creek Garden listing_e is a conditional candidate pending written fee and child-damage terms, and Mingcheng Court listing_b is eliminated for the 83-minute route. Route, elevator, rent, and evidence timestamps are retained together.")
    elif stage == 13:
        await _list_calendar(rec)
        for date in ("2026-07-28", "2026-07-30", "2026-08-04", "2026-08-06"):
            await rec.call("calendar", "create_event", {"summary": "sister date-specific pickup backup", "start": f"{date}T17:30:00+08:00", "end": f"{date}T18:15:00+08:00", "description": f"Sister Lily Li limited assistance on {date}; date-specific backup only, not ongoing and not assumed without confirmation.", "location": "Mingcheng Road Primary School", "calendar_id": CALENDAR_ID})
        if not vars.get("e_question_draft"):
            await rec.call("email", "save_draft", {"to": "zhou@owner.invalid", "subject": "South Creek Garden elevator, deposit, child occupancy, and viewing window questions", "body": "Please confirm the elevator status, deposit and child-damage deposit, child occupancy, and available viewing window for South Creek Garden. Please provide written refund conditions and document requirements. This draft has no child documents attached and is not an appointment.", "in_reply_to": None})
            vars["e_question_draft"] = True
        await _notion(rec, "Lily Li's limited assistance is recorded on July 28, July 30, August 4, and August 6 as four date-specific backup dates, not ongoing care. The South Creek Garden question draft covers elevator, deposit, child occupancy, documents, and viewing window without attachments or an external appointment.")
    elif stage == 14:
        await _list_calendar(rec)
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_school_early_release"})
        await _notion(rec, "School calendar refresh: early dismissal now runs from 2026-07-27 through 2026-08-07, with pickup at 16:35 and aftercare only through 17:20. The pickup recovery plan and calendar were rechecked after the heat notice.")
    elif stage == 15:
        await _list_calendar(rec)
        await _morning(rec, "2026-07-18", ("Yunanli",))
        await rec.call("maps", "directions", {"origin": ROUTE_VALUES["Hexi South Digital Services Center"], "dest": ROUTE_VALUES["Mingcheng Road Primary School"], "mode": "driving", "depart_at": "2026-07-27T16:20:00+08:00"})
        await rec.call("maps", "directions", {"origin": ROUTE_VALUES["Mingcheng Road Primary School"], "dest": ROUTE_VALUES["Yunanli"], "mode": "driving", "depart_at": "2026-07-27T16:50:00+08:00"})
        await _notion(rec, "Care coverage matrix for the 2026-07-27 to 2026-08-07 workdays: early dismissal at 16:35, aftercare to 17:20, office-to-school pickup, evening route home, and date-specific sister backup are evaluated per day. Yunanli remains the transportation backup; the long-term care plan does not assume sister availability.")
    elif stage == 16:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_e"})
        emails = await rec.call("email", "search_emails", {"query": "\u513f\u7ae5\u635f\u574f\u62bc\u91d1", "folder": "INBOX", "page": 1, "page_size": 50})
        if not any(str(row.get("email_id") or row.get("id") or "") == "300" for row in _rows(emails, "emails", "items", "results")):
            raise RuntimeError("email.search_emails omitted the child-deposit message")
        await rec.call("email", "read_email", {"email_id": "300"})
        await _notion(rec, "South Creek Garden listing_e now carries a CNY 3000 child-damage deposit with unknown and unclear refund conditions. Monthly rent is separated from this one-time charge; written clarification is required for refund conditions and charges outside monthly rent, so the fee is an unresolved risk.")
    elif stage == 17:
        await rec.call("email", "read_email", {"email_id": "300"})
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_e"})
        await _notion(rec, "Child-damage deposit risk for South Creek Garden listing_e: CNY 3000 is pending written confirmation of refund conditions, deduction scope, and custody. Viewing time, deposit terms, and documents are split into separate confirmation items; confirm separately, record the fee risk, keep the appointment unconfirmed, and do not send by default. Child documents are not sent by default and no non-H viewing is scheduled.")
    elif stage == 18:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_h"})
        await rec.call("maps", "get_place_details", {"place_id": "place_h"})
        await rec.call("maps", "get_place_details", {"place_id": "poi_h_market"})
        await _route(rec, "Clearwave Residence", "Mingcheng Road Primary School", "2026-07-27T07:20:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-27T07:55:00+08:00")
        await rec.call("maps", "directions", {"origin": ROUTE_VALUES["Clearwave Residence"], "dest": ROUTE_VALUES["Clearwave Neighborhood Fresh Market"], "mode": "walking", "depart_at": "2026-07-27T18:00:00+08:00"})
        await rec.call("review_platform", "list_reviews", {"merchant_id": "mer_h", "limit": 50})
        await _notion(rec, "Clearwave Residence listing_h is added as a verification candidate, not an automatic first choice: two-bedroom, CNY 7,480 monthly rent, operational elevator, delivery by 2026-08-06, zero child-damage deposit, and no school claim. The school transportation chain and route, fresh-food supermarket walk, elevator evidence, and night noise remain pending on-site verification as separate checks.")
    elif stage == 19:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_h"})
        await rec.call("maps", "get_place_details", {"place_id": "place_h"})
        await _route(rec, "Clearwave Residence", "Mingcheng Road Primary School", "2026-07-27T07:20:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-27T07:55:00+08:00")
        await rec.call("review_platform", "list_reviews", {"merchant_id": "mer_h", "limit": 50})
        await rec.call("calendar", "get_event", {"event_id": "evt_mingcheng_parent_meeting", "calendar_id": CALENDAR_ID})
        await _list_calendar(rec)
        await rec.call("email", "read_email", {"email_id": "301"})
        await _notion(rec, "Clearwave Residence is elevated to a verification candidate after checking the operational elevator, route, and resident review. The email confirms a July 31 18:30 viewing window and that child or school documents are not required to submit. The retimed parent meeting is 17:40-18:20, leaving insufficient buffer; viewing remains pending user decision and no schedule_viewing call is made here.")
    elif stage == 20:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_c"})
        await _route(rec, "Hexi Qingyuan", "Mingcheng Road Primary School", "2026-07-28T07:20:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-28T07:55:00+08:00")
        await _notion(rec, "Hexi Qingyuan listing_c price refresh: the monthly rent is now CNY 7350 after the price cut. The price cut does not change the route hard constraint: the chain remains over limit at 75 minutes with the school drop-off stop, so listing_c is eliminated; history is retained.")
    elif stage == 21:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_c"})
        await _route(rec, "Hexi Qingyuan", "Mingcheng Road Primary School", "2026-07-29T07:20:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-29T07:55:00+08:00")
        await rec.call("email", "read_email", {"email_id": "301"})
        await _notion(rec, "Price-drop review keeps Hexi Qingyuan eliminated because its route remains over the 75-minute hard constraint. Clearwave Residence's 18:30 July 31 viewing window and no-document-submission boundary are organized for later authorization; no appointment is created at this stage.")
    elif stage == 22:
        await rec.call("listing_platform", "schedule_viewing", {"user_id": USER_ID, "listing_id": "listing_h", "datetime": "2026-07-31T18:30:00+08:00"})
        await rec.call("calendar", "create_event", {"summary": "Clearwave Residence listing_h viewing", "start": "2026-07-31T18:30:00+08:00", "end": "2026-07-31T19:30:00+08:00", "description": "Authorized viewing for listing_h / Clearwave Residence. Do not submit child or school documents; school-district eligibility remains unverified. No payment or contract action.", "location": "Clearwave Residence", "calendar_id": CALENDAR_ID})
        await rec.call("calendar", "create_event", {"summary": "Viewing travel buffer: office to Clearwave Residence", "start": "2026-07-31T18:05:00+08:00", "end": "2026-07-31T18:30:00+08:00", "description": "25-minute viewing buffer from the office to Clearwave Residence; viewing buffer and calendar conflict are tracked.", "location": "Hexi South Digital Services Center to Clearwave Residence", "calendar_id": CALENDAR_ID})
        await rec.call("calendar", "update_event", {"event_id": "evt_mingcheng_parent_meeting", "calendar_id": CALENDAR_ID, "status": "cancelled", "description": "Parent meeting cancelled in the family calendar because the authorized Clearwave Residence viewing uses the confirmed window."})
        await _notion(rec, "User confirmation received for the specific Clearwave Residence listing_h viewing on July 31 at 18:30. The calendar contains the viewing and a 25-minute office-to-viewing buffer; the conflicting parent meeting is cancelled. The record explicitly says do not submit child or school documents, and no payment, holding fee, or contract action was taken.")
    elif stage == 23:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "listing_h"})
        await rec.call("maps", "get_place_details", {"place_id": "place_h"})
        await rec.call("maps", "get_place_details", {"place_id": "poi_h_market"})
        await _route(rec, "Clearwave Residence", "Mingcheng Road Primary School", "2026-07-27T07:20:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-27T07:55:00+08:00")
        await rec.call("maps", "directions", {"origin": ROUTE_VALUES["Clearwave Residence"], "dest": ROUTE_VALUES["Clearwave Neighborhood Fresh Market"], "mode": "walking", "depart_at": "2026-07-27T18:00:00+08:00"})
        await rec.call("review_platform", "list_reviews", {"merchant_id": "mer_h", "limit": 50})
        await _list_calendar(rec)
        await _notion(rec, "Last verification before viewing: Clearwave Residence listing_h, the school transportation chain, operational elevator, fresh-food supermarket walk, resident review, viewing calendar event, travel buffer, and cancelled parent meeting were refreshed on 2026-07-31. Child documents remain outside the viewing submission boundary; unresolved night-noise and written fee questions stay visible.")
    elif stage == 24:
        await _notion(rec, "On-site observation for Clearwave Residence: elevator operational status and hallway/bedroom condition are recorded as observed; night noise requires a second listening and remains unconfirmed. The inspection classification is evidence only and the family should not sign or pay until unresolved risks are confirmed.")
    elif stage == 25:
        for lid in ("listing_h", "listing_c", "listing_e"):
            await rec.call("listing_platform", "get_listing_detail", {"listing_id": lid})
        await rec.call("maps", "get_place_details", {"place_id": "place_h"})
        await rec.call("maps", "get_place_details", {"place_id": "poi_h_market"})
        await _route(rec, "Clearwave Residence", "Mingcheng Road Primary School", "2026-07-27T07:20:00+08:00")
        await _route(rec, "Mingcheng Road Primary School", "Hexi South Digital Services Center", "2026-07-27T07:55:00+08:00")
        await rec.call("maps", "directions", {"origin": ROUTE_VALUES["Clearwave Residence"], "dest": ROUTE_VALUES["Clearwave Neighborhood Fresh Market"], "mode": "walking", "depart_at": "2026-07-27T18:00:00+08:00"})
        await _list_calendar(rec)
        await rec.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await rec.call("review_platform", "list_reviews", {"merchant_id": "mer_h", "limit": 50})
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_school_early_release"})
        await _notion(rec, "Final rental archive: Clearwave Residence listing_h is first choice subject to unresolved night noise and written confirmation; Yunanli listing_d is the transportation backup; Hexi Qingyuan listing_c remains eliminated for the route hard constraint despite the CNY 7350 price cut; Mingcheng Court listing_b remains eliminated after the 83-minute detour chain; South Creek Garden listing_e remains conditional because of the CNY 3000 child-damage deposit with unknown refund conditions. The morning and evening transportation chain, pickup plan, early dismissal care coverage matrix, calendar conflict, parent meeting cancellation, elevator and route evidence, privacy boundary, child documents do not send externally rule, unresolved risks, next steps, next-step confirmation, and user confirmation are archived. The viewingbuffer is recorded; viewing is the only confirmed external action; no payment, holding fee, signing, contract, school claim, or sensitive attachment was made.")
    else:
        raise ValueError(f"unsupported virtual stage: {stage}")
    completed.append(stage)
    state["events"].append({"step": spec.get("step"), "stage": stage, "deferred": False})


ACTION_HANDLERS = {"record_event": _handle_record_event}


def _trajectory(spec: dict[str, Any], recorder: Recorder, response: str) -> None:
    messages: list[dict[str, Any]] = []
    for call in recorder.calls:
        messages.extend([
            {"role": "assistant", "content": [{"type": "toolCall", "id": call["tool_call_id"], "name": call["function_name"], "arguments": call["arguments"]}]},
            {"role": "tool", "content": [{"type": "toolResult", "tool_use_id": call["tool_call_id"], "content": json.dumps(call["result"], ensure_ascii=False, default=str)}]},
        ])
    messages.append({"role": "assistant", "content": response})
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "trajectory.json").write_text(json.dumps({"steps": [{"name": spec.get("step"), "messages": messages}]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


async def run(spec: dict[str, Any]) -> None:
    state = _load_state()
    recorder = Recorder()
    for action in spec.get("actions", []):
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    _save_state(state)
    style = os.environ.get("ORACLE_STYLE", "canonical").strip().lower()
    if style == "canonical":
        response = RESPONSE
    elif style == "paraphrase":
        response = str(spec.get("response_paraphrase") or "")
        if not response.strip():
            raise ValueError("step spec missing non-empty response_paraphrase")
    else:
        raise ValueError(f"unsupported ORACLE_STYLE: {style!r}")
    _trajectory(spec, recorder, response)
    print(response)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: oracle.py step_spec.json")
    asyncio.run(run(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
