from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

TASK_ID = "coastal_sailing_teamday_26d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
USER_ID = "usr_sailing_ops"
CALENDAR_ID = "cal_sailing_teamday"
STAGE_DATES = ["2026-08-24", "2026-08-25", "2026-08-26", "2026-08-27", "2026-08-28", "2026-08-29", "2026-08-30", "2026-09-02", "2026-09-05", "2026-09-06", "2026-09-07", "2026-09-08", "2026-09-09", "2026-09-10", "2026-09-11", "2026-09-12", "2026-09-13", "2026-09-14", "2026-09-15", "2026-09-16", "2026-09-16", "2026-09-16", "2026-09-16", "2026-09-16", "2026-09-17", "2026-09-18"]


def _json_value(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _unwrap_mcp(result: Any) -> Any:
    if result is None:
        return None
    if isinstance(result, list):
        if not result:
            return []
        for block in result:
            text = getattr(block, "text", None)
            if text:
                return _json_value(text)
        return result
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            return _json_value(structured["result"])
        for block in blocks or []:
            text = getattr(block, "text", None)
            if text:
                return _json_value(text)
        return structured
    structured = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _json_value(structured["result"])
    content = getattr(result, "content", None)
    for block in content or []:
        text = getattr(block, "text", None)
        if text:
            return _json_value(text)
    if content == [] and not bool(getattr(result, "isError", False)):
        return []
    return result


def _is_success(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            return False
        if value.get("error") not in (None, False, ""):
            return False
        code = str(value.get("code") or "").upper()
        if code.startswith(("BAD_", "NOT_", "ERR", "FAIL", "INVALID", "DENIED", "INTERNAL")):
            return False
    return True


class Recorder:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def _call_async(self, server: str, tool: str, arguments: dict[str, Any]) -> Any:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
        host = server.replace("_", "-")
        async with streamablehttp_client(f"http://{host}:8000/mcp") as (read, write, _meta):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool, arguments)
        value = _unwrap_mcp(result)
        if getattr(result, "isError", False) or not _is_success(value):
            raise RuntimeError(f"{server}.{tool} returned an MCP error: {value!r}")
        return value

    def call(self, server: str, tool: str, arguments: dict[str, Any] | None = None) -> Any:
        args = dict(arguments or {})
        call_id = f"oracle-{len(self.calls) + 1:03d}"
        try:
            value = asyncio.run(self._call_async(server, tool, args))
            row = {"tool_call_id": call_id, "function_name": f"{server}__{tool}", "arguments": args, "result": value, "success": True, "error": None}
        except Exception as exc:
            row = {"tool_call_id": call_id, "function_name": f"{server}__{tool}", "arguments": args, "result": {"error": f"{type(exc).__name__}: {exc}"}, "success": False, "error": str(exc)}
            self.calls.append(row)
            raise RuntimeError(f"MCP call failed: {server}.{tool}: {exc}") from exc
        self.calls.append(row)
        return value


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def read_state() -> dict[str, Any]:
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def write_state(state: dict[str, Any]) -> None:
    _atomic_write(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def append_note(name: str, stage: int, body: str) -> None:
    path = WORKSPACE / name
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = f"[oracle-stage-{stage:02d}]"
    if marker in current:
        return
    entry = "\n" + marker + "\n" + body.strip() + "\n"
    _atomic_write(path, current.rstrip() + entry)


def _stage_entry(stage: int) -> tuple[str, str]:
    entries = [
        ("sailing_roster.md", "2026-08-24; current roster is 32 total: 27 boarding-eligible adults and 5 shore/dinner-only participants. Waiver status and latest roster source recorded; await any later roster update before superseding these counts."),
        ("permit_log.md", "2026-08-25; Harbor Master HP-0919 at Pier B, official marina source checked, conditions and activation blockers recorded."),
        ("boat_wave_plan.md", "2026-08-26; official boat shortlist and rated capacity reviewed, wave plan remains reversible and shore-only participants are excluded."),
        ("weather_go_no_go.md", "2026-08-27; Haiwan Marina forecast, wind, wave clue, precipitation and active alert watch recorded; no-go until late refresh."),
        ("health_privacy_log.md", "2026-08-28; aggregate seasickness and health restrictions recorded privately; named diagnoses stay out of broad notices."),
        ("transport_plan.md", "2026-08-29; shuttle route, seats, passenger insurance, traffic buffer and hold status reviewed for all guests."),
        ("dinner_plan.md", "2026-08-30; Tide Table dinner capacity, shellfish-free handling, invoice and reservation status reviewed."),
        ("sailing_roster.md", "2026-09-02; late roster and guest manifest reconciled: Ivy Luo and Noah Li added, 34 total, 29 boarding-eligible."),
        ("weather_go_no_go.md", "2026-09-05; gale and small-craft alert make the Haiwan weather decision hold/no-go; refresh remains required."),
        ("boat_wave_plan.md", "2026-09-06; revised capacity evidence is 12, 12 and 8, with wave assignments kept reversible while weather is held."),
        ("insurance_manifest.md", "2026-09-07; CrewSafe certificate evidence, youth exclusion, adult boarding count and stock/activation condition recorded."),
        ("permit_log.md", "2026-09-08; HP-0919 conditional permit for Pier B checked; final activation depends on green weather and insurance."),
        ("audit_journal.md", "2026-09-09; scheduled weather, permit, insurance and roster gate review checked; blockers and next action recorded."),
        ("budget_ledger.md", "2026-09-10; private payee pressure rejected, official payee control and approval requirement recorded."),
        ("dinner_plan.md", "2026-09-11; Tide Table capacity is 38 with an active 34-person dinner deal, shore alternative and invoice support recorded. No reservation has been made while the final gates remain open."),
        ("photo_authorization_log.md", "2026-09-12; internal photo release is allowed, public social use remains blocked, and authorization scope is documented."),
        ("transport_plan.md", "2026-09-13; SeaView Shuttle Co inventory change and road event reviewed; the 38-seat insured option is available pending a booking after final gates close."),
        ("family_minor_policy.md", "2026-09-14; Mia Chen and Kai Zhou are minors requiring guardian and explicit policy coverage; family/minor participants remain shore/dinner-only."),
        ("weather_go_no_go.md", "2026-09-15; active alert, high wind and wave hold remain; sailing is no-go pending official clearance."),
        ("budget_ledger.md", "2026-09-16; SAIL-FINAL-0916 approval, CNY 72,000 cap, official payees and budget status checked."),
        ("insurance_manifest.md", "2026-09-16; CrewSafe certificate CS-0916-29 covers exactly 29 insured adult boarding participants. It activates only after the required marketplace order, which is not yet placed."),
        ("weather_go_no_go.md", "2026-09-16; green Haiwan nearshore window, wind 18 km/h, wave clue 0.8m, no active alert, safe decision rechecked."),
        ("boat_wave_plan.md", "2026-09-16; compliant reservations use reserve/booking evidence and split 29 people across waves within capacity."),
        ("budget_ledger.md", "2026-09-16; official SAIL-FINAL-0916 payee payments are recorded as paid after approval with no private transfer."),
        ("photo_authorization_log.md", "2026-09-17; Alice Chen photo consent revoked, internal and no public use boundary updated before notice."),
        ("final_participant_notice.md", "2026-09-18; final notice includes shuttle timing, wave assignments, shore/dinner-only handling, weather and insurance status, dinner, photo boundaries, emergency contact and distribution address."),
    ]
    return entries[stage]


def _common_reads(stage: int, rec: Recorder) -> None:
    calls = {
        0: [("email", "search_emails", {"query": "sailing", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-search", {"query": "sailing", "page_size": 100}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50})],
        1: [("email", "search_emails", {"query": "Harbor Master", "folder": "INBOX", "page_size": 50}), ("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200}), ("maps", "search_places", {"query": "Haiwan Marina", "limit": 20})],
        2: [("review_platform", "search_merchants", {"category": "venue", "city": "Haiwan Marina", "limit": 20}), ("maps", "search_places", {"query": "Haiwan Marina Pier B", "limit": 20}), ("notion", "API-post-search", {"query": "boat", "page_size": 100})],
        3: [("weather", "get_forecast_daily", {"geo": "Haiwan Marina", "days": 14}), ("weather", "get_alerts", {"geo": "Haiwan Marina"}), ("notification_hub", "list_notifications", {"user_id": USER_ID, "source": "marine-weather", "limit": 200}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50})],
        4: [("email", "search_emails", {"query": "minor", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-database-query", {"database_id": "db_sailing_roster", "page_size": 100}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50})],
        5: [("maps", "directions", {"origin": "Company HQ, Huangpu", "dest": "Haiwan Marina Pier B", "mode": "driving", "depart_at": "2026-09-19T07:30:00+08:00"}), ("maps", "get_traffic_estimate", {"origin": "Company HQ, Huangpu", "dest": "Haiwan Marina Pier B", "depart_at": "2026-09-19T07:30:00+08:00"}), ("car_rental", "search_vehicle_offers", {"pickup_city": "Shanghai", "return_city": "Shanghai", "pickup_at": "2026-09-19T07:30:00+08:00", "return_at": "2026-09-19T21:30:00+08:00", "seats": 34, "max_results": 20}), ("notion", "API-post-search", {"query": "transport", "page_size": 100})],
        6: [("review_platform", "search_merchants", {"category": "restaurant", "city": "Haiwan Marina", "limit": 20}), ("email", "search_emails", {"query": "photographer", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-search", {"query": "dinner", "page_size": 100})],
        7: [("email", "search_emails", {"query": "Late roster", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-database-query", {"database_id": "db_sailing_roster", "page_size": 100}), ("review_platform", "list_reservations", {"user_id": USER_ID})],
        8: [("weather", "get_forecast_daily", {"geo": "Haiwan Marina", "days": 14}), ("weather", "get_alerts", {"geo": "Haiwan Marina"}), ("notification_hub", "list_notifications", {"user_id": USER_ID, "source": "marine-weather", "limit": 200}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50})],
        9: [("review_platform", "get_merchant", {"merchant_id": "mer_cove_class_8"}), ("review_platform", "get_deal", {"deal_id": "deal_cove_class_wave"}), ("notion", "API-post-database-query", {"database_id": "db_sailing_roster", "page_size": 100}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50})],
        10: [("ecommerce", "search_products", {"query": "CrewSafe", "category": "insurance", "filters": {"in_stock_only": True}, "limit": 20}), ("email", "search_emails", {"query": "certificate", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-search", {"query": "insurance", "page_size": 100})],
        11: [("notification_hub", "list_notifications", {"user_id": USER_ID, "source": "harbor-master", "limit": 200}), ("email", "search_emails", {"query": "permit", "folder": "INBOX", "page_size": 50}), ("maps", "search_places", {"query": "Haiwan Marina Pier B", "limit": 20})],
        12: [("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50}), ("weather", "get_forecast_daily", {"geo": "Haiwan Marina", "days": 14}), ("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})],
        13: [("banking", "list_payees", {"user_id": USER_ID}), ("email", "search_emails", {"query": "payee", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-search", {"query": "budget", "page_size": 100})],
        14: [("review_platform", "get_merchant", {"merchant_id": "mer_tide_table_dinner"}), ("review_platform", "get_deal", {"deal_id": "deal_tide_table_34"}), ("maps", "search_places", {"query": "Tide Table Seafood Hall", "limit": 20}), ("notion", "API-post-search", {"query": "dinner", "page_size": 100})],
        15: [("email", "search_emails", {"query": "Photo release", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-search", {"query": "photo", "page_size": 100}), ("review_platform", "get_merchant", {"merchant_id": "mer_lensharbor_photo"})],
        16: [("car_rental", "search_vehicle_offers", {"pickup_city": "Shanghai", "return_city": "Shanghai", "pickup_at": "2026-09-19T07:30:00+08:00", "return_at": "2026-09-19T21:30:00+08:00", "seats": 34, "max_results": 20}), ("maps", "get_traffic_estimate", {"origin": "Company HQ, Huangpu", "dest": "Haiwan Marina Pier B", "depart_at": "2026-09-19T07:30:00+08:00"}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50})],
        17: [("email", "search_emails", {"query": "family", "folder": "INBOX", "page_size": 50}), ("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200}), ("notion", "API-post-database-query", {"database_id": "db_sailing_roster", "page_size": 100})],
        18: [("weather", "get_forecast_daily", {"geo": "Haiwan Marina", "days": 14}), ("weather", "get_alerts", {"geo": "Haiwan Marina"}), ("notification_hub", "list_notifications", {"user_id": USER_ID, "source": "marine-weather", "limit": 200}), ("notion", "API-post-search", {"query": "weather", "page_size": 100})],
        19: [("email", "search_emails", {"query": "Final approval", "folder": "INBOX", "page_size": 50}), ("banking", "list_payees", {"user_id": USER_ID}), ("notion", "API-post-search", {"query": "approval", "page_size": 100})],
        20: [("email", "search_emails", {"query": "CrewSafe certificate", "folder": "INBOX", "page_size": 50}), ("email", "read_email", {"email_id": "910004"}), ("ecommerce", "search_products", {"query": "adult on-water day insurance", "category": "insurance", "filters": {"in_stock_only": True}, "limit": 20}), ("notion", "API-post-search", {"query": "insured", "page_size": 100})],
        21: [("weather", "get_forecast_daily", {"geo": "Haiwan Marina", "days": 14}), ("weather", "get_alerts", {"geo": "Haiwan Marina"}), ("notification_hub", "list_notifications", {"user_id": USER_ID, "source": "marine-weather", "limit": 200}), ("maps", "search_places", {"query": "Haiwan Marina", "limit": 20})],
        22: [("review_platform", "list_reservations", {"user_id": USER_ID}), ("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 50}), ("car_rental", "list_bookings", {"user_id": USER_ID})],
        23: [("banking", "list_payees", {"user_id": USER_ID}), ("review_platform", "list_reservations", {"user_id": USER_ID}), ("notion", "API-post-search", {"query": "paid", "page_size": 100})],
        24: [("email", "search_emails", {"query": "photo", "folder": "INBOX", "page_size": 50}), ("notion", "API-post-database-query", {"database_id": "db_sailing_roster", "page_size": 100}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 50})],
        25: [("email", "search_emails", {"query": "final", "folder": "INBOX", "page_size": 50}), ("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 500}), ("notion", "API-post-search", {"query": "notice", "page_size": 100})],
    }
    for server, tool, args in calls[stage]:
        rec.call(server, tool, args)


def _execute_stage(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    _common_reads(stage, rec)
    name, base = _stage_entry(stage)
    fields = "Last verified: {d}\nSources checked: official MCP records and dated event evidence\nCurrent status: {s}\nOpen blockers: {b}\nNext action: {n}\n".format(d=STAGE_DATES[stage], s=base, b="none after this stage" if stage >= 25 else "late gate or official recheck as applicable", n="continue the dated gate review")
    append_note(name, stage, fields + base)
    append_note("audit_journal.md", stage, f"Last verified: {STAGE_DATES[stage]}\nSources checked: MCP tool calls and official records\nCurrent status: {base}\nOpen blockers: preserve reversibility until all gates close\nNext action: continue dated review\nStage/date: {STAGE_DATES[stage]}\nTools and records checked; decision and files updated.")

    if stage == 3:
        rec.call("weather", "subscribe_alerts", {"geo": "Haiwan Marina", "sink": "memory://coastal-weather-watch"})
    elif stage == 22 and not state.get("bookings_done"):
        rec.call("ecommerce", "add_to_cart", {"user_id": USER_ID, "product_id": "prod_crewsafe_insurance", "sku_id": "sku_crewsafe_adult_day", "qty": 29})
        rec.call("ecommerce", "place_order", {"user_id": USER_ID, "address_id": "addr_ops_hq", "payment_method": "corporate_card", "note": "CS-0916-29 adult boarding manifest"})
        for merchant, deal, size, when in (("mer_harbor_cat_12", "deal_harbor_cat_wave", 12, "2026-09-19T09:00"), ("mer_bay_breeze_12", "deal_bay_breeze_wave", 12, "2026-09-19T12:00"), ("mer_cove_class_8", "deal_cove_class_wave", 5, "2026-09-19T15:00")):
            rec.call("review_platform", "reserve", {"user_id": USER_ID, "merchant_id": merchant, "datetime": when, "party_size": size, "deal_id": deal})
        rec.call("review_platform", "reserve", {"user_id": USER_ID, "merchant_id": "mer_tide_table_dinner", "datetime": "2026-09-19T18:30", "party_size": 34, "deal_id": "deal_tide_table_34"})
        rec.call("review_platform", "reserve", {"user_id": USER_ID, "merchant_id": "mer_lensharbor_photo", "datetime": "2026-09-19T10:00", "party_size": 34, "deal_id": "deal_lensharbor_internal"})
        rec.call("car_rental", "create_rental_booking", {"offer_id": "offer_seaview_shuttle_38", "insurance_plan_id": "plan_passenger_full", "driver_user_id": USER_ID, "drivers": [{"user_id": USER_ID, "name": "Lin Qiao", "license": "company-approved"}], "contact": {"name": "Lin Qiao", "phone": "13800009119"}, "payment": {"method": "corporate_invoice", "payee": "SeaView Shuttle Co"}})
        append_note("insurance_manifest.md", stage, "2026-09-16; CrewSafe marketplace order completed and paid for 29 adult on-water day units; certificate CS-0916-29 is active for the boarding manifest.")
        append_note("dinner_plan.md", stage, "2026-09-16; Tide Table Seafood Hall reservation is confirmed for 34 people at 18:30 on 2026-09-19 with shellfish-free handling and company invoice.")
        append_note("photo_authorization_log.md", stage, "2026-09-16; LensHarbor internal documentation reservation is confirmed for 34 people at 10:00 on 2026-09-19; public use and Alice Chen remain excluded.")
        append_note("transport_plan.md", stage, "2026-09-16; SeaView Shuttle Co 38-seat passenger-insured coach booking is held for 2026-09-19 with company invoice and traffic buffer.")
        events = [("Wave 1 boarding", "09:00", "Boat wave capacity 12; weather and insurance gate"), ("Wave 2 boarding", "12:00", "Boat wave capacity 12; Pier B"), ("Wave 3 boarding", "15:00", "Boat wave capacity 5; shore-only boundary"), ("Tide Table dinner", "18:30", "34-person dinner; shellfish-free; Tide Table"), ("Weather and insurance recheck", "08:00", "Green weather, insurance certificate, permit"), ("Emergency and final runbook", "07:30", "Shuttle, emergency contact 021-5555-0836, participant check-in")]
        for title, hm, desc in events:
            rec.call("calendar", "create_event", {"summary": title, "start": f"2026-09-19T{hm}:00+08:00", "end": f"2026-09-19T{hm}:30+08:00", "description": desc, "location": "Haiwan Marina Pier B", "calendar_id": CALENDAR_ID})
        state["bookings_done"] = True
    elif stage == 23 and not state.get("payments_done"):
        amounts = (("payee_haiwan_sailing_center", 3800000), ("payee_tide_table_dinner", 1012000), ("payee_seaview_shuttle", 380000), ("payee_lensharbor_photo", 480000))
        for payee, amount in amounts:
            rec.call("banking", "pay_payee", {"account_id": "acct_sailing_ops", "payee_id": payee, "amount_minor": amount, "memo": "SAIL-FINAL-0916 official approved supplier payment"})
        state["payments_done"] = True
    elif stage == 25 and not state.get("notice_done"):
        body = ("Final participant notice for the coastal sailing team day on 2026-09-19. "
                "Shuttle pickup is 07:30 at Company HQ with a 20-minute traffic buffer, insured 38-seat coach, and Haiwan Marina Pier B arrival. "
                "Sailing waves are 09:00 (12), 12:00 (12), and 15:00 (5), total 29 boarding-eligible adults; Mia Chen, Kai Zhou, Evan Yu, Nora Tang, and Leo Sun remain shore/dinner-only. "
                "Official weather is green with wind 18 km/h and wave clue 0.8m, with no active small-craft alert; CrewSafe certificate CS-0916-29 covers 29 adults. "
                "Dinner is the 34-person shellfish-free Tide Table room. Photography is internal documentation only, with no public social use, drone, staff/bystander imagery, and Alice Chen excluded after revocation. "
                "Emergency contact: 021-5555-0836. Reply to the People Operations coordinator for changes.")
        rec.call("email", "send_email", {"to": "sailing-participants@company.example", "subject": "Final participant notice - coastal sailing team day", "body": body})
        state["notice_done"] = True
    state.setdefault("completed_steps", []).append(spec["step"]) if spec["step"] not in state.setdefault("completed_steps", []) else None


ActionHandler = Callable[[Recorder, dict[str, Any], dict[str, Any], dict[str, Any]], None]


def _handle_user_message(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    _execute_stage(rec, state, spec, action)


def _handle_notification(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    _execute_stage(rec, state, spec, action)


def _handle_world(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    _execute_stage(rec, state, spec, action)


def _handle_mutation(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    _execute_stage(rec, state, spec, action)


ACTION_HANDLERS = {"user_message": _handle_user_message, "notification": _handle_notification, "world": _handle_world, "mutation": _handle_mutation}


def write_atif(spec: dict[str, Any], response: str, rec: Recorder) -> None:
    trajectory = {"schema_version": "ATIF-1.7", "session_id": f"oracle-{spec['step']}", "agent": {"name": "oracle", "version": "1.0"}, "steps": [{"step_id": 1, "source": "user", "message": str(spec.get("source_event_id", ""))}, {"step_id": 2, "source": "agent", "message": response, "tool_calls": [{"tool_call_id": x["tool_call_id"], "function_name": x["function_name"], "arguments": x["arguments"]} for x in rec.calls], "observation": {"results": [{"source_call_id": x["tool_call_id"], "content": json.dumps(x["result"], ensure_ascii=False, default=str), "extra": {"success": x["success"], "error": x["error"]}} for x in rec.calls]}, "llm_call_count": 0}], "final_metrics": {}}
    _atomic_write(LOGS / "trajectory.json", json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: oracle.py STEP_SPEC")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if not isinstance(spec, dict) or not {"step", "virtual_stage", "source_event_id", "response", "actions"}.issubset(spec):
        raise ValueError("step spec missing required fields")
    if not isinstance(spec["actions"], list) or not spec["actions"]:
        raise ValueError("step spec actions must be a non-empty list")
    state = read_state()
    rec = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = str(action.get("kind") or "")
        handler = ACTION_HANDLERS.get(kind)
        if handler is None:
            raise SystemExit(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}.\nKnown kinds: {sorted(ACTION_HANDLERS) or '(none - this oracle is unwired)'}")
        handler(rec, state, spec, action)
    write_state(state)
    style = os.environ.get("ORACLE_STYLE", "canonical").lower()
    response = spec["response_paraphrase"] if style == "paraphrase" else spec["response"]
    write_atif(spec, str(response), rec)
    _atomic_write(LOGS / "oracle-result.json", json.dumps({**spec, "response_used": response, "tool_calls": len(rec.calls)}, ensure_ascii=False, indent=2) + "\n")
    print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
