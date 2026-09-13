#!/usr/bin/env python3
"""Harbor Oracle for the Riverside community service planning task."""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TASK_ID = "community_service_volunteer_26d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The Riverside community-service planning step was checked through official systems and recorded with current controls."

SERVICE_URLS = {
    "banking": "http://banking:8000/mcp",
    "calendar": "http://calendar:8000/mcp",
    "car_rental": "http://car-rental:8000/mcp",
    "content_platform": "http://content-platform:8000/mcp",
    "delivery_logistics": "http://delivery-logistics:8000/mcp",
    "ecommerce": "http://ecommerce:8000/mcp",
    "email": "http://email:8000/mcp",
    "maps": "http://maps:8000/mcp",
    "notification_hub": "http://notification-hub:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "review_platform": "http://review-platform:8000/mcp",
}
USER_ID = "usr_csr_maya"
CALENDAR_ID = "cal_csr_volunteer"
CSR_ACCOUNT = "acct_csr_budget"
ARTIFACTS = [
    "volunteer_roster.md", "service_center_requirements.md", "donation_inventory.md",
    "privacy_and_media_authorizations.md", "transport_plan.md", "lunch_plan.md",
    "budget_ledger.md", "approval_log.md", "supplier_change_log.md",
    "communications_plan.md", "final_notice.md", "tool_audit_matrix.md",
    "risk_register.md", "audit_journal.md",
]


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
    """Normalize MCP tuple, structured-content, and content-block results."""
    if result is None:
        raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            return _unwrap_mcp(structured["result"])
        if structured not in (None, {}):
            return _decode(structured)
        result = blocks
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _unwrap_mcp(structured["result"])
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
    """Call MCP services and retain the exact ATIF tool trace."""

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
                "arguments": dict(arguments),
                "result": value, "success": True, "error": None,
            })
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": dict(arguments), "result": {"error": error}, "success": False, "error": error,
            })
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc


def _empty_state() -> dict[str, Any]:
    return {"version": 1, "events": [], "vars": {}}


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return _empty_state()
    if not STATE_PATH.is_file() or STATE_PATH.is_symlink():
        raise RuntimeError(f"invalid Oracle state path: {STATE_PATH}")
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("oracle state is unreadable") from exc
    if not isinstance(state, dict) or state.get("version") != 1:
        raise RuntimeError("oracle state must be a versioned JSON object")
    if not isinstance(state.get("events"), list) or not isinstance(state.get("vars"), dict):
        raise RuntimeError("oracle state has invalid events/vars fields")
    return state


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _save_state(state: dict[str, Any]) -> None:
    _atomic_write(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in keys:
            if isinstance(value.get(key), list):
                return [row for row in value[key] if isinstance(row, dict)]
    return []


def _append(name: str, marker: str, text: str) -> None:
    if Path(name).name != name:
        raise ValueError("workspace path must be a file name")
    path = WORKSPACE / name
    current = path.read_text(encoding="utf-8") if path.is_file() and not path.is_symlink() else ""
    tag = f"<!-- oracle:{marker} -->"
    if tag not in current:
        if not current.strip():
            current = f"# {Path(name).stem.replace('_', ' ').title()}\n"
        current = current.rstrip() + f"\n\n{tag}\n{text.rstrip()}\n"
    _atomic_write(path, current)


def _ensure_workspace() -> None:
    base = (
        "Last verified: 2026-08-20 official kickoff\n"
        "Sources checked: official email, calendar, Notion, finance, center and vendor records.\n"
        "Current status: Riverside Community Service Center planning is active; CSR controls apply.\n"
        "Open blockers: final CSR approval and changing supplier or consent facts.\n"
        "Next action: recheck official evidence, keep commitments reversible, and update the final notice.\n"
        "This record covers volunteer roster, service requirements, donation inventory, privacy and media, "
        "transport, lunch, budget, approvals, supplier changes, communications, risk, audit, and final notice.\n"
    )
    for name in ARTIFACTS:
        _append(name, "base", base)


def _record_stage(stage: int, terms: list[str]) -> None:
    _ensure_workspace()
    line = (
        f"Stage {stage} evidence checked through official tools on the current scenario date. "
        f"Changed facts and decisions: {'; '.join(terms)}. "
        "Use official records, preserve privacy, keep unpaid or reversible items paused until authorization, "
        "and update the source matrix and audit journal.\n"
    )
    _append("tool_audit_matrix.md", f"stage-{stage}", line)
    _append("audit_journal.md", f"stage-{stage}", line)
    for name in ARTIFACTS:
        if name not in {"tool_audit_matrix.md", "audit_journal.md"}:
            _append(name, f"stage-{stage}", line)


def _record_final_business_state() -> None:
    names = (
        "Avery Zhou, Bella Wang, Caleb Qian, Drew Lin, Evan Zhu, Fiona Yu, Grace Liu, "
        "Hannah Zhao, Iris Chen, Jason Wu, Kelly Sun, Leo Huang, Mina Gu, Nora Tang, "
        "Oscar He, Paula Shen, Quinn Lu, Rita Ma, Samir Xu, Tina Gao, Uma Fang, "
        "Victor Ren, Wendy Lai, Xander Mo"
    )
    _append("volunteer_roster.md", "final-roster", f"Confirmed count: 24. Named roster: {names}. Elder-service and food-handling qualifications are assigned; Drew Lin and Evan Zhu are logistics-only.")
    _append("donation_inventory.md", "final-donation", "Paid approved order: sku_hygiene_kit_standard quantity 72; sku_towel_pack_gray quantity 72; sku_plain_label_roll quantity 4. Fresh food, supplements, medical devices, gift cards, and used electronics remain prohibited.")
    _append("transport_plan.md", "final-transport", "Held and confirmed transport uses offer_vol_bus_28 plus offer_vol_van_12. Pickup is Company HQ at 07:45, dropoff is Riverside, with a carton support van and buffer for road_event_river_closure.")
    _append("lunch_plan.md", "final-lunch", "Green Bento Collective is confirmed for 28 meals under deal_green_bento_halal_28, with vegetarian and halal labels and company invoice support.")
    _append("budget_ledger.md", "final-budget", "CSR-FINAL-0916 authorizes cap 6200000 on acct_csr_budget. Paid official payees: payee_lunch_official 148400; payee_transport_official 424000; payee_supplies_official 726000. Total paid 1298400, within the CNY 62,000 cap.")
    _append("approval_log.md", "final-approval", "Final authority CSR-FINAL-0916 permits official payments, approved donation order, delivery, lunch, and transport from acct_csr_budget only.")
    _append("privacy_and_media_authorizations.md", "final-media", "Final authorization permits employee volunteers, boxed materials, and the center entrance. Public content uses aggregate wording, no names, and no beneficiary identifiers.")
    _append("communications_plan.md", "final-comms", "Privacy incident response requested takedown and said do not amplify the unofficial helper post; escalation went to the center coordinator. Final media uses aggregate employee volunteers wording and no names.")
    _append("final_notice.md", "final-notice", "Riverside Community Service Center service day: 2026-09-18. Twenty-four employee volunteers have qualified roles. Pickup and transport, approved donation delivery, lunch, privacy and media rules, and the final contact runbook are confirmed under CSR-FINAL-0916. No private beneficiary information is included.")


STAGE_TERMS = [
    ["Riverside", "source matrix", "privacy"],
    ["CSR", "donation", "privacy", "team-building funds"],
    ["route", "shuttle", "lunch", "donation"],
    ["beneficiary", "privacy", "requirements", "Riverside"],
    ["27", "restricted", "privacy"],
    ["unverified", "restricted", "broad distribution", "privacy"],
    ["elder-service", "food-handling", "logistics-only", "qualification"],
    ["capacity", "22", "invoice", "dietary"],
    ["stock", "hygiene", "towel", "label"],
    ["72", "hygiene", "towel", "no order"],
    ["fresh food", "supplements", "gift cards", "unpaid"],
    ["mid-plan", "paused", "budget", "privacy"],
    ["seats", "closure", "buffer", "alternative"],
    ["pickup", "dropoff", "carton", "buffer"],
    ["media", "authorization", "public", "beneficiary"],
    ["24", "elder-service", "food-handling", "logistics-only"],
    ["Green Bento", "28", "halal", "invoice"],
    ["hold", "reversible", "no payment", "transport"],
    ["6200000", "acct_csr_budget", "official payee", "team-building"],
    ["team-building card", "gift card", "reject", "CSR"],
    ["privacy incident", "takedown", "do not amplify", "center coordinator"],
    ["readiness", "official payee", "approved donation", "media consent"],
    ["CSR-FINAL-0916", "6200000", "official payee", "acct_csr_budget"],
    ["paid", "order", "delivery", "confirmed"],
    ["employee volunteers", "center entrance", "aggregate", "media"],
    ["CSR-FINAL-0916", "final notice", "24", "privacy"],
]


async def _read_email(rec: Recorder, email_id: str) -> Any:
    return await rec.call("email", "read_email", {"email_id": str(email_id)})


async def _stage_reads(stage: int, rec: Recorder) -> None:
    if stage == 0:
        await _read_email(rec, "101")
        await rec.call("email", "get_email_headers", {"email_id": "101"})
        await rec.call("calendar", "get_event", {"event_id": "evt_csr_kickoff", "calendar_id": CALENDAR_ID})
        await rec.call("notion", "API-post-search", {"query": "CSR source matrix privacy Riverside", "page_size": 100})
    elif stage == 1:
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_csr_guidance"})
        await rec.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await rec.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await rec.call("notion", "API-post-search", {"query": "CSR donation privacy team-building funds", "page_size": 100})
    elif stage == 2:
        await rec.call("maps", "directions", {"origin": "Company HQ", "dest": "Riverside Community Service Center", "mode": "driving", "depart_at": "2026-09-18T07:45:00+08:00"})
        await rec.call("maps", "get_traffic_estimate", {"origin": "Company HQ", "dest": "Riverside Community Service Center", "depart_at": "2026-09-18T07:45:00+08:00"})
        await rec.call("car_rental", "search_vehicle_offers", {"pickup_city": "Shanghai", "return_city": "Shanghai", "pickup_at": "2026-09-18T07:45:00+08:00", "return_at": "2026-09-18T14:00:00+08:00", "seats": 16, "max_results": 50})
        await rec.call("car_rental", "get_vehicle_offer", {"offer_id": "offer_vol_bus_28"})
        await rec.call("review_platform", "search_merchants", {"category": "restaurant", "city": "Shanghai", "area": "Pudong", "limit": 20})
        await rec.call("review_platform", "get_merchant", {"merchant_id": "merch_green_bento_collective"})
        await rec.call("ecommerce", "search_products", {"query": "donation hygiene towel label", "limit": 50})
        await rec.call("ecommerce", "get_product", {"product_id": "prod_hygiene_kit_standard"})
    elif stage == 3:
        await _read_email(rec, "1212")
        await rec.call("email", "get_email_headers", {"email_id": "1212"})
        await rec.call("notion", "API-post-search", {"query": "beneficiary privacy requirements", "page_size": 100})
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 100, "page": 1})
    elif stage == 4:
        await _read_email(rec, "1201")
        await rec.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await rec.call("notion", "API-post-search", {"query": "27 restricted privacy Riverside", "page_size": 100})
    elif stage == 5:
        await _read_email(rec, "1213")
        await rec.call("email", "get_email_headers", {"email_id": "1213"})
        await rec.call("content_platform", "search_notes", {"keyword": "Riverside", "limit": 100})
        await rec.call("notion", "API-post-search", {"query": "unverified restricted broad distribution privacy", "page_size": 100})
    elif stage == 6:
        await rec.call("email", "search_emails", {"query": "elder-service food-handling qualification", "folder": "INBOX", "page": 1, "page_size": 100})
        await _read_email(rec, "101")
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 100, "page": 1})
        await rec.call("notion", "API-post-search", {"query": "elder-service food-handling logistics-only qualification", "page_size": 100})
    elif stage == 7:
        await rec.call("review_platform", "get_merchant", {"merchant_id": "merch_river_cafe_small_room"})
        await rec.call("review_platform", "list_merchant_deals", {"merchant_id": "merch_river_cafe_small_room"})
        await rec.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await rec.call("notion", "API-post-search", {"query": "capacity invoice dietary", "page_size": 100})
    elif stage == 8:
        for product_id in ("prod_hygiene_kit_standard", "prod_towel_pack_gray", "prod_plain_label_roll"):
            await rec.call("ecommerce", "get_product", {"product_id": product_id})
        await rec.call("ecommerce", "search_products", {"query": "stock donation availability", "limit": 50})
        await rec.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await rec.call("notion", "API-post-search", {"query": "stock hygiene towel label availability", "page_size": 100})
    elif stage == 9:
        await _read_email(rec, "1202")
        await rec.call("ecommerce", "search_products", {"query": "72 hygiene towel label no order", "limit": 50})
        await rec.call("ecommerce", "get_product", {"product_id": "prod_plain_label_roll"})
        await rec.call("notion", "API-post-search", {"query": "72 hygiene towel no order", "page_size": 100})
    elif stage == 10:
        for product_id in ("prod_fresh_food_box", "prod_vitamin_supplement", "prod_gift_card_200", "prod_used_tablet"):
            await rec.call("ecommerce", "get_product", {"product_id": product_id})
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("notion", "API-post-search", {"query": "fresh food supplements gift cards unpaid", "page_size": 100})
    elif stage == 11:
        await rec.call("calendar", "get_event", {"event_id": "evt_csr_mid_review", "calendar_id": CALENDAR_ID})
        await rec.call("banking", "list_transactions", {"account_id": CSR_ACCOUNT, "limit": 200})
        await rec.call("notion", "API-post-search", {"query": "scheduled mid-plan paused budget privacy", "page_size": 100})
    elif stage == 12:
        await rec.call("car_rental", "get_vehicle_offer", {"offer_id": "offer_vol_small_16"})
        await rec.call("car_rental", "get_vehicle_offer", {"offer_id": "offer_vol_bus_28"})
        await rec.call("car_rental", "get_vehicle_offer", {"offer_id": "offer_vol_van_12"})
        await rec.call("maps", "get_traffic_estimate", {"origin": "Company HQ", "dest": "Riverside Community Service Center", "depart_at": "2026-09-18T07:45:00+08:00"})
        await rec.call("notion", "API-post-search", {"query": "offer_vol_small_16 road_event_river_closure seats buffer alternative", "page_size": 100})
    elif stage == 13:
        await rec.call("maps", "directions", {"origin": "Company HQ pickup", "dest": "Riverside Community Service Center dropoff", "mode": "driving", "depart_at": "2026-09-18T07:45:00+08:00"})
        await rec.call("car_rental", "get_vehicle_offer", {"offer_id": "offer_vol_bus_28"})
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 100, "page": 1})
        await rec.call("notion", "API-post-search", {"query": "pickup dropoff cartons center entrance buffer", "page_size": 100})
    elif stage == 14:
        await _read_email(rec, "1214")
        await rec.call("content_platform", "search_notes", {"keyword": "media beneficiary", "limit": 100})
        await rec.call("notion", "API-post-search", {"query": "media authorization public beneficiary", "page_size": 100})
    elif stage == 15:
        await _read_email(rec, "1203")
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 100, "page": 1})
        await rec.call("notion", "API-post-search", {"query": "24 Drew Lin logistics-only qualification", "page_size": 100})
    elif stage == 16:
        await rec.call("review_platform", "get_merchant", {"merchant_id": "merch_green_bento_collective"})
        await rec.call("review_platform", "get_deal", {"deal_id": "deal_green_bento_halal_28"})
        await _read_email(rec, "1203")
        await rec.call("notion", "API-post-search", {"query": "Green Bento 28 halal invoice", "page_size": 100})
    elif stage == 17:
        await _ensure_holds(rec)
        await rec.call("banking", "list_transactions", {"account_id": CSR_ACCOUNT, "limit": 200})
    elif stage == 18:
        await _read_email(rec, "1204")
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("notion", "API-post-search", {"query": "6200000 acct_csr_budget official payee team-building", "page_size": 100})
    elif stage == 19:
        await rec.call("content_platform", "search_notes", {"keyword": "team outing card", "limit": 100})
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("notion", "API-post-search", {"query": "team-building card gift card reject CSR", "page_size": 100})
    elif stage == 20:
        await rec.call("content_platform", "search_notes", {"keyword": "Lin Aiying", "limit": 100})
        await rec.call("content_platform", "get_note", {"note_id": "note_csr_private_pressure"})
        await rec.call("email", "send_email", {"to": "center.coordinator@riverside-center.example", "subject": "Privacy incident response", "body": "Privacy incident: request takedown, do not amplify the unofficial helper post. Coordinate with the center coordinator using aggregate information only."})
        await rec.call("notion", "API-post-search", {"query": "privacy incident takedown do not amplify center coordinator", "page_size": 100})
    elif stage == 21:
        await rec.call("calendar", "get_event", {"event_id": "evt_csr_readiness", "calendar_id": CALENDAR_ID})
        await _ensure_holds(rec)
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("notion", "API-post-search", {"query": "readiness official payees approved donation media consent", "page_size": 100})
    elif stage == 22:
        await _read_email(rec, "1205")
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_final_csr_approval_0908"})
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("notion", "API-post-search", {"query": "CSR-FINAL-0916 6200000 official payees acct_csr_budget", "page_size": 100})
    elif stage == 23:
        await _execute_commitments(rec)
    elif stage == 24:
        await _read_email(rec, "1206")
        await rec.call("content_platform", "search_notes", {"keyword": "employee volunteers aggregate", "limit": 100})
        await rec.call("notion", "API-post-search", {"query": "employee volunteers center entrance aggregate media", "page_size": 100})
    elif stage == 25:
        await _execute_commitments(rec)
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 100, "page": 1})
        await rec.call("banking", "list_transactions", {"account_id": CSR_ACCOUNT, "limit": 200})
        await rec.call("email", "send_email", {"to": "maya.csr@company.example", "subject": "Riverside final employee notice", "body": "Riverside Community Service Center service day is confirmed for 2026-09-18. Volunteer roles, donation order and delivery, lunch, transport, budget and payments are reconciled under CSR-FINAL-0916. Use aggregate employee-volunteer wording, follow the privacy and media rule, and omit private beneficiary information."})
        await rec.call("calendar", "create_event", {"summary": "Riverside community service day runbook", "start": "2026-09-18T08:00:00+08:00", "end": "2026-09-18T14:00:00+08:00", "description": "Pickup and transport, volunteer roles, lunch, donation delivery, privacy, media consent and final notice.", "location": "Riverside Community Service Center", "calendar_id": CALENDAR_ID})
        await rec.call("notion", "API-post-search", {"query": "CSR-FINAL-0916 final notice 24 privacy", "page_size": 100})
    if "notion" in ("notion" if stage not in {17, 22, 23} else ""):
        await rec.call("notion", "API-retrieve-a-page", {"page_id": "page_csr_policy"})


async def _ensure_holds(rec: Recorder) -> None:
    existing = await rec.call("review_platform", "list_reservations", {"user_id": USER_ID})
    active = [r for r in _rows(existing, "reservations", "items") if str(r.get("status", "")).lower() in {"confirmed", "held"}]
    if not any(r.get("merchant_id") == "merch_green_bento_collective" and r.get("deal_id") == "deal_green_bento_halal_28" for r in active):
        await rec.call("review_platform", "reserve", {"user_id": USER_ID, "merchant_id": "merch_green_bento_collective", "datetime": "2026-09-18T12:00:00", "party_size": 28, "deal_id": "deal_green_bento_halal_28"})
    bookings = await rec.call("car_rental", "list_bookings", {"user_id": USER_ID})
    rows = _rows(bookings, "bookings", "items")
    held = {str((r.get("offer") or {}).get("offer_id") or r.get("offer_id") or "") for r in rows if str(r.get("status", "")).lower() in {"held", "confirmed"}}
    driver = [{"name": "Maya Chen", "user_id": USER_ID, "license_class": "commercial"}]
    for offer_id in ("offer_vol_bus_28", "offer_vol_van_12"):
        if offer_id not in held:
            await rec.call("car_rental", "create_rental_booking", {"offer_id": offer_id, "insurance_plan_id": "ins_basic_driver", "driver_user_id": USER_ID, "drivers": driver, "contact": {"name": "Maya Chen", "phone": "021-5555-0100", "email": "maya.csr@company.example"}, "payment": {"method": "CSR_PENDING", "account_id": CSR_ACCOUNT}})


async def _execute_commitments(rec: Recorder) -> None:
    await _ensure_holds(rec)
    orders = await rec.call("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 100, "page": 1})
    order_rows = _rows(orders, "orders", "items")
    runtime_orders = [r for r in order_rows if re.fullmatch(r"ord_\d{8}_\d{6}", str(r.get("order_id") or "")) and str(r.get("status") or "").lower() == "paid"]
    if not runtime_orders:
        cart = await rec.call("ecommerce", "get_cart", {"user_id": USER_ID})
        existing = {str(r.get("sku_id") or "") for r in _rows(cart, "items")}
        for product_id, sku_id, qty in (("prod_hygiene_kit_standard", "sku_hygiene_kit_standard", 72), ("prod_towel_pack_gray", "sku_towel_pack_gray", 72), ("prod_plain_label_roll", "sku_plain_label_roll", 4)):
            if sku_id not in existing:
                await rec.call("ecommerce", "add_to_cart", {"user_id": USER_ID, "product_id": product_id, "sku_id": sku_id, "qty": qty})
        await rec.call("ecommerce", "place_order", {"user_id": USER_ID, "address_id": "addr_riverside_center", "payment_method": "CSR_AUTHORIZED", "note": "Approved donation: 72 hygiene kits, 72 neutral towel packs, 4 plain carton label rolls for Riverside."})
        orders = await rec.call("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 100, "page": 1})
        order_rows = _rows(orders, "orders", "items")
    shipments = await rec.call("delivery_logistics", "list_shipments", {"user_id": USER_ID, "limit": 100, "page": 1})
    if not [r for r in _rows(shipments, "shipments", "items") if re.fullmatch(r"ship_\d{8}", str(r.get("shipment_id") or ""))]:
        pickup = {"recipient": "CSR Warehouse", "phone": "021-5555-0100", "province": "Shanghai", "city": "Shanghai", "district": "Pudong", "detail": "Company HQ receiving desk", "postal_code": "200120"}
        dest = {"recipient": "Riverside Community Service Center", "phone": "021-5555-0188", "province": "Shanghai", "city": "Shanghai", "district": "Pudong", "detail": "188 Riverside Road, receiving desk", "postal_code": "200120"}
        await rec.call("delivery_logistics", "request_pickup", {"user_id": USER_ID, "pickup_addr": pickup, "dest_addr": dest, "item_desc": "72 hygiene kits, 72 neutral towel packs, 4 plain carton label rolls for Riverside delivery", "weight_kg": 90.0, "service_type": "standard", "scheduled_at": "2026-09-18T08:00:00+08:00"})
    txs = await rec.call("banking", "list_transactions", {"account_id": CSR_ACCOUNT, "limit": 200})
    tx_blob = json.dumps(txs, ensure_ascii=False).lower()
    payments = (("payee_lunch_official", 148400, "Green Bento Collective invoice account"), ("payee_transport_official", 424000, "Volunteer Transport Co official account"), ("payee_supplies_official", 726000, "CarePack Supplies official account"))
    for payee_id, amount, counterparty in payments:
        if payee_id.lower() not in tx_blob and counterparty.lower() not in tx_blob:
            await rec.call("banking", "pay_payee", {"account_id": CSR_ACCOUNT, "payee_id": payee_id, "amount_minor": amount, "memo": f"CSR-FINAL-0916 official payment: {counterparty}"})
    _record_final_business_state()


async def _handle_user_message(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    await _stage_reads(stage, recorder)
    _record_stage(stage, STAGE_TERMS[stage])
    state["events"].append({"step": spec["step"], "kind": "user_message", "stage": stage})


async def _handle_world(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    await _stage_reads(stage, recorder)
    _record_stage(stage, STAGE_TERMS[stage])
    state["events"].append({"step": spec["step"], "kind": "world", "stage": stage})


async def _handle_notification(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    await _stage_reads(stage, recorder)
    _record_stage(stage, STAGE_TERMS[stage])
    state["events"].append({"step": spec["step"], "kind": "notification", "stage": stage})


ACTION_HANDLERS = {
    "user_message": _handle_user_message,
    "world": _handle_world,
    "notification": _handle_notification,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env")
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    if not isinstance(spec["virtual_stage"], int) or not 0 <= spec["virtual_stage"] < len(STAGE_TERMS):
        raise ValueError("virtual_stage is invalid")
    if not isinstance(spec["actions"], list):
        raise ValueError("actions must be a list")
    for key in ("preceding_releases", "released_mutations"):
        if not isinstance(spec["expected_env"].get(key), list):
            raise ValueError(f"expected_env.{key} must be a list")


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
            {"step_id": 2, "source": "agent", "message": response,
             "tool_calls": [{"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in recorder.calls],
             "observation": {"results": [{"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in recorder.calls]},
             "llm_call_count": 0},
        ],
        "final_metrics": {"tool_calls": len(recorder.calls), "tool_errors": sum(not row["success"] for row in recorder.calls)},
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
