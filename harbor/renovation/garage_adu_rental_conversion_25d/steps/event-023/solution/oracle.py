#!/usr/bin/env python3
from __future__ import annotations
import asyncio
import json
import os
from pathlib import Path
from typing import Any

TASK_ID = "garage_adu_rental_conversion_25d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
STAGE = 20
RESPONSE = "I reread the new reinspection schedule and refreshed the materials and contractor dates instead of using stale entries."
PLAN = [["calendar","get_event",{"event_id":"evt_adu_reinspect_0822","calendar_id":"cal_main"}],["calendar","search_events",{"query":"reinspection","time_min":"2026-08-21T00:00:00+08:00","time_max":"2026-08-23T00:00:00+08:00","max_results":20}],["review_platform","get_deal",{"deal_id":"deal_inspect_recheck_a20"}],["ecommerce","get_product",{"product_id":"prod_alarm_alt"}]]

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
    for block in content or []:
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
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        urls = json.loads(os.environ.get("HARBOR_MCP_URLS", "{}"))
        url = urls.get(service, f"http://{service.replace('_', '-')}:8000/mcp")
        call_id = f"call-{len(self.calls) + 1}"
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
            row = {"id":call_id,"name":f"{service}__{tool}","arguments":arguments,"result":value,"succeeded":True}
            self.calls.append(row)
            return value
        except Exception as exc:
            value = {"error": f"{type(exc).__name__}: {exc}"}
            self.calls.append({"id":call_id,"name":f"{service}__{tool}","arguments":arguments,"result":value,"succeeded":False})
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

def _write_workspace(stage: int) -> None:
    control = """# ADU control
Property: 18 Cedar Lane detached garage accessory dwelling unit (ADU).
Scope: residential conversion with independent entrance, bathroom, kitchenette, insulation, daylight and ventilation.
Zoning eligibility and residential building permit status are tracked against case ADU-26-0803.
Required preconditions: emergency egress, smoke/CO alarms, utility connection plan, parking/access solution, inspection status, and permit status.
Go/no-go: the unit cannot be treated as lawful rental housing until the official file is complete and the inspection is passed.
"""
    budget = """# Budget ledger
Build budget cap: CNY 240000. Track permits, design, structure/windows, insulation, bathroom, kitchenette, electrical, alarms, inspection, and contingency.
"""
    if stage >= 2:
        budget += "Oakview ADU market read: 910000 minor units, CNY 9100 per month. Rent payback is separate from the construction budget.\n"
    if stage >= 10:
        budget += "Committed and awaiting-authorization lines remain separate; contingency is not committed and no cash payment is made.\n"
    contractor = """# Contractor matrix
Harbor CodeBuild (ctr_code): licensed, insured, ADU permit experience, written contract, fixed-price scope, and inspection coordination.
Budget Backyard Studio Crew (ctr_budget): lower price but cash-only, optional egress/alarm, and no contract; rejected.
"""
    if stage >= 9:
        contractor += "The personal-account cash request is rejected; no payment or signing is authorized without a written contract and insurance certificate.\n"
    if stage >= 16:
        contractor += "Harbor CodeBuild reservation is recorded for a site meeting; contract, insurance, permit scope, and payment milestones remain explicit.\n"
    materials = """# Materials log
Candidate classes: egress clear-opening casement window, smoke/CO alarm, fire-rated insulation, and bathroom exhaust.
Each row records specification, stock update, price, suitability, and return terms before purchase.
"""
    if stage >= 12:
        materials += "The CodeGuard bundle reached stock 0; SafeNest sku_alarm_alt is the in-stock replacement. EgressPro window price is recorded after the update.\n"
    parking = """# Parking neighbor log
A documented parking/access solution remains in the plan for 18 Cedar Lane. Neighbor communication covers access lane use, construction noise, and schedule.
No false promise changes lawful rental use; written notices and permit status control.
"""
    guard = """# Tenant listing guardrail
Only confirmed, permitted, compliant residential ADU features may appear in tenant advertising.
A storage, workshop, studio, or office description cannot replace the dwelling-use plan. Public launch is held until permit status and inspection status are confirmed.
"""
    if stage >= 18:
        guard += "After the failed rough inspection, no public rental listing is allowed until remediation and a later pass.\n"
    if stage >= 21:
        guard += "The pass is recorded; listing copy remains limited to confirmed egress, alarm, ventilation, parking, and independent entrance.\n"
    if stage >= 23:
        guard += "Confirmed features only: lawful rental advertising describes the permitted ADU, egress, smoke/CO alarms, parking/access, and independent entrance.\n"
    inspection = """# Inspection handoff
Permit correction package and pre-inspection evidence are tracked for ADU-26-0803.
"""
    if stage >= 18:
        inspection += "Rough inspection ADU-RI-0819 failed: egress clear opening, dedicated bathroom exhaust, and alarm drawing locations require remediation. Rental advertising is not allowed during the hold.\n"
    if stage >= 21:
        inspection += "Reinspection passed under ADU-FI-0822; egress, alarm, and ventilation evidence are confirmed after the prior failure.\n"
    audit = """# Audit journal
Sources are the legal_search, notification_hub, listing_platform, review_platform, ecommerce, email, calendar, and notion records.
"""
    if stage >= 24:
        audit += "Final cross-check: permit case ADU-26-0803, CNY 240000 build budget, CNY 9100 rent payback kept separate, material order, Harbor CodeBuild contract boundary, parking/access, inspection transition, confirmed listing, and open go/no-go risks.\n"
    for name, value in {"adu_control.md":control,"budget_ledger.md":budget,"contractor_matrix.md":contractor,"materials_log.md":materials,"tenant_listing_guardrail.md":guard,"parking_neighbor_log.md":parking,"inspection_handoff.md":inspection,"audit_journal.md":audit}.items():
        _write(name, value)

def _find(value: Any, key: str) -> str | None:
    if isinstance(value, dict):
        if value.get(key):
            return str(value[key])
        for child in value.values():
            found = _find(child, key)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find(child, key)
            if found:
                return found
    return None

async def handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    for service, tool, arguments in PLAN:
        await recorder.call(service, tool, arguments)
    if STAGE == 12:
        await recorder.call("ecommerce","get_cart",{"user_id":"marina"})
        await recorder.call("ecommerce","add_to_cart",{"user_id":"marina","product_id":"prod_window_code","sku_id":"sku_window_code","qty":1})
        await recorder.call("ecommerce","add_to_cart",{"user_id":"marina","product_id":"prod_alarm_alt","sku_id":"sku_alarm_alt","qty":1})
        order = await recorder.call("ecommerce","place_order",{"user_id":"marina","address_id":"addr_adu","payment_method":"authorized_material_purchase","note":"Code-relevant egress window and SafeNest alarm."})
        order_id = _find(order,"order_id")
        if order_id:
            state["order_id"] = order_id
    if STAGE == 14:
        event = await recorder.call("calendar","create_event",{"summary":"ADU permit inspection contractor compliance review","start":"2026-08-14T15:00:00+08:00","end":"2026-08-14T16:00:00+08:00","description":"Permit review, inspection, contractor meeting, and pre-launch compliance.","location":"18 Cedar Lane","calendar_id":"cal_main"})
        event_id = _find(event,"event_id")
        if event_id:
            state["calendar_event_id"] = event_id
    if STAGE == 16:
        reservation = await recorder.call("review_platform","reserve",{"user_id":"marina","merchant_id":"ctr_code","datetime":"2026-08-17T09:00:00","party_size":1})
        reservation_id = _find(reservation,"reservation_id")
        if reservation_id:
            state["reservation_id"] = reservation_id
    if STAGE == 23:
        listing = await recorder.call("listing_platform","post_listing",{"user_id":"marina","category":"rent","title":"Confirmed Oakview ADU at 18 Cedar Lane","price_minor":910000,"city":"Harbor City","district":"Oakview","community":"Oakview","area_sqm":28,"rooms":1,"metro":"Harbor City transit","description":"Permitted compliant ADU dwelling with confirmed egress, SafeNest smoke and carbon monoxide alarms, parking/access solution, and independent entrance.","attrs":{"legal_status":"permitted ADU","egress":"confirmed","alarms":"smoke and carbon monoxide alarms","parking":"confirmed","inspection_status":"passed"},"photos":[]})
        listing_id = _find(listing,"listing_id")
        if listing_id:
            state["listing_id"] = listing_id
    state["last_stage"] = STAGE
    _write_workspace(STAGE)

def _trajectory(spec: dict[str, Any], recorder: Recorder, response: str) -> None:
    messages: list[dict[str, Any]] = []
    for call in recorder.calls:
        messages.extend([{"role":"assistant","content":[{"type":"toolCall","id":call["id"],"name":call["name"],"arguments":call["arguments"]}]},{"role":"tool","content":[{"type":"toolResult","tool_use_id":call["id"],"content":json.dumps(call["result"],ensure_ascii=True,default=str)}]}])
    messages.append({"role":"assistant","content":response})
    LOGS.mkdir(parents=True,exist_ok=True)
    (LOGS/"trajectory.json").write_text(json.dumps({"steps":[{"name":spec.get("step"),"messages":messages}]},ensure_ascii=True,indent=2)+"\n",encoding="utf-8")

async def run(spec: dict[str, Any]) -> None:
    state = _load_state()
    recorder = Recorder()
    for action in spec.get("actions",[]):
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder,state,spec,action)
    _save_state(state)
    _trajectory(spec,recorder,RESPONSE)
    print(RESPONSE)

ACTION_HANDLERS = {"record_event": handle_record_event}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise SystemExit("usage: oracle.py step_spec.json")
    asyncio.run(run(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
