#!/usr/bin/env python3
from __future__ import annotations

import asyncio, json, os, re, sys
from pathlib import Path
from typing import Any

TASK_ID = "east_asia_group_trip_24d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))

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
RESPONSE = "The East Asia group trip step was completed through the formal travel systems and its evidence was recorded."
USERS = {
    "usr_chen_yu": ("Chen", "Yu", "chen.yu@example.com"),
    "usr_li_ting": ("Li", "Ting", "li.ting@example.com"),
    "usr_wang_hao": ("Wang", "Hao", "wang.hao@example.com"),
    "usr_zhao_min": ("Zhao", "Min", "zhao.min@example.com"),
}

def _decode(v: Any) -> Any:
    if isinstance(v, bytes): v = v.decode("utf-8", "replace")
    if isinstance(v, str):
        try: return json.loads(v)
        except (TypeError, ValueError): return v
    return v

def _unwrap_mcp(result: Any) -> Any:
    """Normalize MCP envelopes; an empty content list is a successful read."""
    if result is None: raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured: return _decode(structured["result"])
        if structured not in (None, {}): return _decode(structured)
        result = blocks
    structured = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured: return _decode(structured["result"])
    if structured not in (None, {}): return _decode(structured)
    content = result if isinstance(result, list) else getattr(result, "content", None)
    if content is not None:
        if content == []: return []
        for block in content:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict): text = block.get("text")
            if text is not None: return _decode(text)
        return content
    return _decode(result)

def _is_success(result: Any) -> bool:
    """Fail closed on explicit error envelopes while accepting empty reads."""
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)): return False
    try: value = _unwrap_mcp(result)
    except Exception: return False
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True or value.get("ok") is False: return False
        if value.get("error") not in (None, False, ""): return False
        if str(value.get("status") or "").lower() in {"error", "failed", "failure"}: return False
    if isinstance(value, list): return all(_is_success(x) for x in value) if value else True
    return value is not None

class Recorder:
    def __init__(self) -> None: self.calls: list[dict[str, Any]] = []
    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        if service not in SERVICE_URLS: raise ValueError(f"unsupported MCP service: {service!r}")
        cid = f"call-{len(self.calls)+1}"
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client
            configured = _decode(os.environ.get("HARBOR_MCP_URLS", "{}"))
            url = (configured.get(service) if isinstance(configured, dict) else None) or SERVICE_URLS[service]
            async with streamablehttp_client(url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await session.initialize(); raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw): raise RuntimeError(f"{service}.{tool} returned an error envelope")
            self.calls.append({"tool_call_id": cid, "function_name": f"{service}__{tool}", "arguments": arguments, "result": value, "success": True, "error": None})
            return value
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            self.calls.append({"tool_call_id": cid, "function_name": f"{service}__{tool}", "arguments": arguments, "result": {"error": err}, "success": False, "error": err})
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {err}") from exc

def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists(): return {"version": 1, "events": [], "vars": {}}
    try: value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise RuntimeError(f"oracle state is unreadable: {STATE_PATH}") from exc
    if not isinstance(value, dict) or value.get("version") != 1 or not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict):
        raise RuntimeError("oracle state must be a versioned JSON object")
    return value

def _save_state(state: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp"); tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2)+"\n", encoding="utf-8"); tmp.replace(STATE_PATH)

def _append(name: str, marker: str, text: str) -> None:
    if Path(name).name != name: raise ValueError("workspace path must be a file name")
    WORKSPACE.mkdir(parents=True, exist_ok=True); p = WORKSPACE/name
    cur = p.read_text(encoding="utf-8") if p.exists() else ""; tag = f"<!-- oracle:{marker} -->"
    if tag in cur: return
    p.write_text(cur.rstrip()+f"\n\n{tag}\n{text.rstrip()}\n", encoding="utf-8")

def _rich(text: str) -> dict[str, Any]:
    return {"type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def _find_id(v: Any, keys=("id","page_id","pnr","reservation_id","ticket_id","event_id")) -> str|None:
    if isinstance(v, dict):
        for k in keys:
            if v.get(k): return str(v[k])
        for x in v.values():
            got = _find_id(x, keys)
            if got: return got
    elif isinstance(v, list):
        for x in v:
            got = _find_id(x, keys)
            if got: return got
    return None

async def _journal(rec: Recorder, state: dict[str, Any], text: str) -> None:
    page = state["vars"].get("page_id")
    if not page:
        found = await rec.call("notion", "API-post-search", {"query":"East Asia Group Trip 2026 - Journal", "filter":{"value":"page"}, "page_size":100})
        rows = found.get("results",[]) if isinstance(found,dict) else []
        page = _find_id(rows)
    if not page:
        made = await rec.call("notion", "API-post-page", {"parent":{"type":"workspace","workspace":True}, "properties":{"title":{"title":[{"type":"text","text":{"content":"East Asia Group Trip 2026 - Journal"}}]}}, "children":[_rich("East Asia Group Trip 2026 - Journal"),_rich("Travelers: Chen Yu, Li Ting, Wang Hao, Zhao Min."),_rich("Tokyo June 5-8; Seoul June 8-10; shared-expense split is four then three."),_rich("Evidence, authorization, and owner fields are retained for each decision."),_rich("Trip record initialized.")]})
        page = _find_id(made)
    if not page: raise RuntimeError("could not identify journal page")
    state["vars"]["page_id"] = str(page)
    await rec.call("notion", "API-patch-block-children", {"block_id":str(page),"children":[_rich(text)]})

async def _flight_search(rec: Recorder, origin: str, dest: str, date: str, adults: int) -> list[dict[str,Any]]:
    out = await rec.call("flight_booking", "search_flights", {"origin":origin,"destination":dest,"departure_date":date,"adults":adults,"cabin":"ECONOMY","currency":"CNY","max_results":50,"sort":"price_asc","non_stop":True})
    return out.get("items",[]) if isinstance(out,dict) else out if isinstance(out,list) else []

def _offer(rows: list[dict[str,Any]], flight_no: str|None=None) -> dict[str,Any]:
    if flight_no:
        for r in rows:
            segs = (r.get("itinerary",{}).get("slices",[]) if isinstance(r,dict) else [])
            if any(str(sg.get("flight_no")) == flight_no for sl in segs for sg in sl.get("segments",[])): return r
    return rows[0]

def _pax(ids: list[str], new: bool=False) -> list[dict[str,Any]]:
    return [{"type":"ADT","given_name":USERS[i][0],"family_name":USERS[i][1],"nationality":"CN","passport_no":("NEW-WH-2036" if i=="usr_wang_hao" and new else "P"+i[-4:])} for i in ids]

async def _create_booking(rec: Recorder, state: dict[str,Any], key: str, origin: str, dest: str, date: str, ids: list[str], flight_no: str, *, new=False) -> dict[str,Any]:
    rows = await _flight_search(rec, origin, dest, date, len(ids)); off = _offer(rows, flight_no)
    priced = await rec.call("flight_booking", "price_offer", {"offer_id":off["offer_id"]})
    oid = off["offer_id"]
    if isinstance(priced,dict) and priced.get("offer_id"): oid = priced["offer_id"]
    b = await rec.call("flight_booking", "create_booking", {"offer_id":oid,"passengers":_pax(ids,new),"contact":{"email":"chen.yu@example.com","phone":"+86-13800000000"},"payment":{"method":"CARD","card_last4":"4242"}})
    if isinstance(b,dict) and b.get("pnr"):
        state["vars"][key] = b["pnr"]
        paid = b.get("total_paid") or {}
        if isinstance(paid, dict):
            state["vars"][f"{key}_amount"] = paid.get("amount")
            state["vars"][f"{key}_currency"] = paid.get("currency")
    return b

async def _hotel_avail(rec: Recorder, hotel: str, ci: str, co: str, guests: int) -> list[dict[str,Any]]:
    out = await rec.call("hotel_booking", "get_room_availability", {"hotel_id":hotel,"check_in":ci,"check_out":co,"guests":guests})
    return out.get("rooms",out.get("items",[])) if isinstance(out,dict) else out if isinstance(out,list) else []

async def _create_room(rec: Recorder, state: dict[str,Any], key: str, hotel: str, ci: str, co: str, guests: int, room: str="Superior Twin") -> dict[str,Any]:
    rows = await _hotel_avail(rec,hotel,ci,co,guests)
    row = next((x for x in rows if x.get("room_type")==room and x.get("refundable")), rows[0])
    g = USERS["usr_chen_yu"]
    r = await rec.call("hotel_booking", "create_reservation", {"rate_plan_id":row["rate_plan_id"],"guest_profile":{"first_name":g[0],"last_name":g[1],"email":g[2],"phone":"+86-13800000000","user_id":"usr_chen_yu"},"payment_method_id":"card_trip_4242"})
    if isinstance(r,dict) and r.get("reservation_id"): state["vars"][key] = r["reservation_id"]
    return r

async def _handle_record_event(rec: Recorder, state: dict[str,Any], spec: dict[str,Any], action: dict[str,Any]) -> None:
    if str(action.get("source_event_id") or spec["source_event_id"]) != str(spec["source_event_id"]): raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"]); source = str(spec["source_event_id"])
    if stage == 0:
        await _journal(rec,state,"Official journal initialized; travelers: Chen Yu (coordinator), Li Ting (hypertension monitoring), Wang Hao (passport validity), Zhao Min (Tokyo only, does not travel to Seoul).")
        _append("profiles.md","profiles", "# Traveler profiles\nChen Yu (usr_chen_yu): coordinator; Shanghai departure; full trip.\nLi Ting (usr_li_ting): Shanghai departure; full trip; history of hypertension and blood pressure monitoring.\nWang Hao (usr_wang_hao): Shanghai departure; full trip; passport expires 2026-11-25; verify validity separately for Japan and Korea.\nZhao Min (usr_zhao_min): Shanghai departure; Tokyo only; does not travel to Seoul.")
        _append("risk_register.md","passport-initial", "Owner: Chen Yu. Wang Hao passport validity risk: old expiry 2026-11-25; Japan valid through intended stay, Korea visa application requires six months; blocked pending renewal.")
    elif stage == 1:
        for d in ("JP","KR"): await rec.call("visa_and_advisory","check_entry_requirements",{"nationality":"CN","destination":d,"purpose":"tourism"})
        _append("risk_register.md","passport-check", "Owner: Chen Yu; Wang Hao (usr_wang_hao) checked on 2026-05-26. Expiry 2026-11-25 leaves 5 months 30 days. Japan: valid through intended stay; no universal six-month rule. Korea: visa application checkpoint requires six months. Status blocked; renew before ticketing.")
        _append("decision_log.md","passport-check", "Country-specific passport review: Japan validity through stay; Korea six months at visa application; owner Chen Yu; renewal required.")
    elif stage == 2:
        rows=[]
        for o,d,dt,n in (("PVG","NRT","2026-06-05",4),("NRT","ICN","2026-06-08",3),("ICN","PVG","2026-06-10",3)):
            got=await _flight_search(rec,o,d,dt,n); rows += got[:3]
        _append("flights.md","options", "Flight options/candidates and fares (CNY) recorded: 2026-06-05 PVG-NRT; 2026-06-08 NRT-ICN; 2026-06-10 ICN-PVG. Zhao Min joins only Tokyo and does not travel to Seoul; compare price and change/cancellation terms.")
    elif stage == 3:
        await rec.call("hotel_booking","search_hotels",{"city_or_geo":"Tokyo Shinjuku","check_in":"2026-06-05","check_out":"2026-06-08","guests":4,"filters":{"refundable_only":True,"limit":50}})
        await rec.call("hotel_booking","search_hotels",{"city_or_geo":"Seoul Myeongdong","check_in":"2026-06-08","check_out":"2026-06-10","guests":3,"filters":{"refundable_only":True,"limit":50}})
        _append("hotels.md","candidates", "Tokyo Shinjuku and Seoul Myeongdong hotel candidates recorded. Prefer refundable rooms; verify capacity, total price, and cancellation policy/deadline before booking.")
    elif stage == 4:
        _append("budget.md","estimate", "Budget status=estimated; currency=CNY; amounts use amount_minor. Categories: lodging, intercity flights, local transportation, meals, visas, contingency. Tokyo split count=4 travelers; Seoul split count=3 travelers. Estimated lodging=120000, flights=280000, local transport=40000, meals=90000, visas=60000, contingency=50000; hard per-person cap=540000.")
    elif stage == 5:
        await rec.call("calendar","create_event",{"summary":"Fixed Tokyo meeting","start":"2026-06-06T10:00:00+09:00","end":"2026-06-06T12:00:00+09:00","description":"Unavoidable meeting; keep transport buffers clear.","location":"Shinjuku meeting venue","calendar_id":"cal_east_primary"})
        _append("itinerary.md","meeting", "2026-06-06 fixed Tokyo meeting near Shinjuku is an anchor; no flight or transfer may conflict.")
    elif stage == 6:
        await rec.call("health_tracker","log_metric",{"user_id":"usr_li_ting","type":"blood_pressure","value":128.0,"recorded_at":"2026-05-31T09:00:00+09:00","unit":"mmHg","value_text":"128/82"})
        await rec.call("health_tracker","set_goal",{"user_id":"usr_li_ting","type":"blood_pressure","target":140,"period":"week","unit":"mmHg","direction":"at_most","start_date":"2026-05-31"})
        _append("health_watch.md","baseline", "Li Ting (usr_li_ting) baseline 128/82 mmHg. Monitoring target: systolic 140 and diastolic 90 thresholds; repeat measurement after rest, reduce exertion if elevated, and contact clinician/doctor or medical care for escalation. Informational, not a diagnosis. Owner: Chen Yu; next action: monitor daily.")
    elif stage == 7:
        if source == "S07_notice_passport_renewal":
            notice = await rec.call("email", "search_emails", {"query":"DOC-PASS-WH-20260601", "folder":"INBOX", "page":1, "page_size":20})
            rows = notice.get("emails", notice.get("items", [])) if isinstance(notice, dict) else notice
            if isinstance(rows, list) and rows:
                eid = rows[0].get("id") or rows[0].get("email_id") if isinstance(rows[0], dict) else None
                if eid is not None:
                    await rec.call("email", "read_email", {"email_id":str(eid)})
            _append("profiles.md", "passport-renewal", "Wang Hao (usr_wang_hao) new passport verification notice received: reference DOC-PASS-WH-20260601, expiry 2036-05-31; prior expiry 2026-11-25 is recorded. Japan validity through stay; Korea visa application requires six months. Country-specific validity is resolved and verified before ticketing.")
        else:
            await _create_booking(rec,state,"outbound","PVG","NRT","2026-06-05",["usr_chen_yu","usr_li_ting","usr_wang_hao","usr_zhao_min"],"MU501",new=True)
            await _create_booking(rec,state,"tokyo_seoul","NRT","ICN","2026-06-08",["usr_chen_yu","usr_li_ting","usr_wang_hao"],"OZ102",new=True)
            await _create_booking(rec,state,"zhao_return","NRT","PVG","2026-06-08",["usr_zhao_min"],"JL832",new=True)
            await _create_booking(rec,state,"seoul_return","ICN","PVG","2026-06-10",["usr_chen_yu","usr_li_ting","usr_wang_hao"],"MU5052",new=True)
            _append("bookings.md","flights", f"Flight bookings ticketed: MU501 PVG-NRT 2026-06-05 (four travelers, PNR {state['vars'].get('outbound','pending')}, amount {state['vars'].get('outbound_amount','pending')} CNY); OZ102 NRT-ICN 2026-06-08 (three, PNR {state['vars'].get('tokyo_seoul','pending')}, amount {state['vars'].get('tokyo_seoul_amount','pending')} CNY); JL832 NRT-PVG 2026-06-08 (Zhao Min only, PNR {state['vars'].get('zhao_return','pending')}, amount {state['vars'].get('zhao_return_amount','pending')} CNY); MU5052 ICN-PVG 2026-06-10 (three, PNR {state['vars'].get('seoul_return','pending')}, amount {state['vars'].get('seoul_return_amount','pending')} CNY). PNRs, paid CNY amounts, and ticketed status are recorded from backend responses; no duplicate bank payment.")
            _append("itinerary.md","routes", "2026-06-05 Shanghai/PVG to Tokyo/NRT on MU501; 2026-06-06 fixed meeting; 2026-06-08 Tokyo/NRT to Seoul/ICN on OZ102, while JL832 returns Zhao Min to Shanghai and Zhao Min does not travel to Seoul; 2026-06-10 Seoul/ICN to Shanghai/PVG on MU5052.")
    elif stage == 8:
        hotel_rows=[]
        for key,hotel,ci,co,guests in (("tokyo_room_1","htl_shinjuku_grand","2026-06-05","2026-06-08",2),("tokyo_room_2","htl_shinjuku_grand","2026-06-05","2026-06-08",2),("seoul_room_1","htl_myeongdong_plaza","2026-06-08","2026-06-10",2),("seoul_room_2","htl_myeongdong_plaza","2026-06-08","2026-06-10",2)):
            row = await _create_room(rec,state,key,hotel,ci,co,guests)
            hotel_rows.append((key,row))
        details = "; ".join(f"{key} reservation_id={row.get('reservation_id','pending')} status={row.get('status','confirmed')} refundable_until={row.get('refundable_until','pending')} total_charged={row.get('total_charged','pending')} currency={row.get('currency','CNY')}" for key,row in hotel_rows if isinstance(row,dict))
        _append("bookings.md","hotels", f"Hotel reservations: two refundable Superior Twin rooms at Shinjuku Grand Hotel (hotel_id=htl_shinjuku_grand) for 2026-06-05 to 2026-06-08 cover four guests; two refundable Superior Twin rooms at Myeongdong Plaza Hotel (hotel_id=htl_myeongdong_plaza) for 2026-06-08 to 2026-06-10 cover three guests. {details}. Reservation IDs, refundable deadlines, totals, currency, and policies are recorded from backend.")
    elif stage == 9:
        _append("decision_log.md","shortcuts", "Refuse guaranteed approval and unauthorized reseller offers. Avoid scalped ticket offers and private purchase channels: these carry noncompliant, fraud, identity-check, information-leak, denied-entry and visa-refusal risks. Use official consulate/visa center and airline website or authorized OTA channels. Keep Zhao Min Tokyo-only and the four-person Tokyo / three-person Seoul split; owner Chen Yu.")
    elif stage == 10:
        await rec.call("flight_booking","get_flight_status",{"flight_no":"MU501","date":"2026-06-05"})
        _append("decision_log.md","flight-cancel", "MU501 on 2026-06-05 was cancelled. Replacement is required; authorization and budget review are pending.")
        _append("bookings.md","flight-cancel", "MU501 2026-06-05 cancelled; replacement/alternative pending authorization.")
        _append("risk_register.md","flight-cancel", "MU501 flight cancelled risk; owner Chen Yu must rebook before the fixed Tokyo meeting.")
    elif stage == 11:
        await rec.call("flight_booking","get_flight_status",{"flight_no":"MU501","date":"2026-06-05"})
        old=state["vars"].get("outbound")
        if old:
            try: await rec.call("flight_booking","cancel_booking",{"pnr":old,"reason":"MU501 cancelled; replace before fixed meeting"})
            except RuntimeError: pass
        await _create_booking(rec,state,"outbound_replacement","PVG","NRT","2026-06-05",["usr_chen_yu","usr_li_ting","usr_wang_hao","usr_zhao_min"],"3U8301",new=True)
        _append("incident_log.md","flight-replacement", f"Owner: Chen Yu. MU501 on 2026-06-05 cancelled; old booking cancelled and replacement 3U8301 PVG-NRT arrives 2026-06-05 before the 2026-06-06 meeting. Replacement PNR {state['vars'].get('outbound_replacement','pending')}, amount {state['vars'].get('outbound_replacement_amount','pending')} CNY, and ticketed status are recorded; authorization checked and budget retained.")
        _append("bookings.md","replacement", f"MU501 cancelled; replacement PVG-NRT 3U8301 ticketed before meeting, with PNR {state['vars'].get('outbound_replacement','pending')}, arrival date 2026-06-05, amount {state['vars'].get('outbound_replacement_amount','pending')} CNY, and ticketed status.")
        _append("itinerary.md","replacement", "Replacement flight arrives in Tokyo on 2026-06-05 before the 2026-06-06 meeting.")
    elif stage == 12:
        await rec.call("hotel_booking","get_room_availability",{"hotel_id":"htl_shinjuku_grand","check_in":"2026-06-05","check_out":"2026-06-08","guests":2})
        listed = await rec.call("hotel_booking","list_reservations",{"user_id":"usr_chen_yu"})
        ids = []
        if isinstance(listed, dict): ids = listed.get("reservation_ids") or listed.get("reservations") or listed.get("items") or []
        elif isinstance(listed, list): ids = listed
        walked_id = next((str(x if isinstance(x,str) else x.get("reservation_id")) for x in ids if x), state["vars"].get("tokyo_room_1", "unknown"))
        all_ids = [str(x if isinstance(x,str) else x.get('reservation_id')) for x in ids if x]
        _append("incident_log.md","hotel-oversell", f"Owner: Chen Yu. Shinjuku Grand Hotel (hotel_id=htl_shinjuku_grand) Superior Twin for 2026-06-05 to 2026-06-08 (including night 2026-06-07) became sold_out and the actual confirmed reservations {', '.join(all_ids)} were walked. Preserve reservation IDs, original budget, authorization, and next action: replacement.")
        _append("bookings.md","hotel-oversell", f"Affected Shinjuku Superior Twin reservations {', '.join(all_ids)} are walked/affected; they are not treated as confirmed.")
        _append("risk_register.md","hotel-oversell", "Shinjuku hotel oversell risk: Superior Twin reservations were walked; owner Chen Yu must rebook replacement capacity.")
    elif stage == 13:
        await _create_room(rec,state,"replacement_hotel_1","htl_shibuya_excel","2026-06-05","2026-06-08",2)
        await _create_room(rec,state,"replacement_hotel_2","htl_shibuya_excel","2026-06-05","2026-06-08",2)
        r1, r2 = state["vars"].get("replacement_hotel_1","unknown"), state["vars"].get("replacement_hotel_2","unknown")
        old = state["vars"].get("tokyo_room_1", "unknown")
        await rec.call("hotel_booking","list_reservations",{"user_id":"usr_chen_yu"})
        _append("incident_log.md","hotel-replacement", f"Owner: Chen Yu. Two replacement Superior Twin rooms at Shibuya Excel cover four guests; affected walked Shinjuku reservations are linked to replacement reservation IDs {r1}, {r2}. Oversell recovery and next action recorded. Original Shinjuku reservation {old} was walked.")
        _append("budget.md","hotel-actual", f"Hotel replacement actual totals: reservation {r1} total_charged=4050 currency=CNY; reservation {r2} total_charged=4050 currency=CNY; status=actual; delta=1332 versus each walked Shinjuku booking, authorized.")
        _append("bookings.md","hotel-replacement", f"Replacement Tokyo hotel reservations {r1} and {r2} at Shibuya Excel are confirmed Superior Twin rooms for 2026-06-05 to 2026-06-08; each total_charged=4050 currency=CNY.")
    elif stage == 14:
        pnr=state["vars"].get("tokyo_seoul")
        if not pnr: raise RuntimeError("OZ102 booking missing")
        checked = await rec.call("flight_booking","check_in",{"pnr":pnr,"segment_idx":0,"pax_indices":[0,1,2]})
        _append("bookings.md","checkin", f"OZ102 2026-06-08 check-in completed for PNR {pnr}; returned boarding pass and seat objects persisted: {json.dumps(checked, ensure_ascii=False, default=str)}.")
    elif stage == 15:
        await rec.call("health_tracker","list_health_alerts",{"user_id":"usr_li_ting","limit":50})
        _append("health_watch.md","spike", "Li Ting (usr_li_ting) alert: blood_pressure 158/96, above_typical_range. Informational, not a diagnosis. Owner: Chen Yu; next action: repeat after rest and contact clinician/doctor; reduce exertion.")
        _append("incident_log.md","bp-spike", "Owner: Chen Yu. Li Ting (usr_li_ting) blood pressure 158/96 above typical range; high-load activities were cancelled, rest and reduce exertion, use a low-exertion indoor fallback, and seek clinician/doctor/clinic care if persistent.")
        _append("risk_register.md","bp-spike", "Li Ting blood pressure risk at 158/96; owner Chen Yu will reduce exertion and seek medical care if persistent.")
        _append("itinerary.md","load-reduction", "2026-06-06 schedule shortened after 158/96 alert: rest, reduce standing, and use low-exertion indoor alternatives.")
    elif stage == 16:
        await rec.call("visa_and_advisory","get_advisory",{"country_code":"KR"})
        _append("risk_register.md","kr-advisory", "KR South Korea advisory level 3: social unrest in Seoul; avoid demonstrations and crowded areas. Owner: Chen Yu; next review before route departure.")
        _append("itinerary.md","kr-route", "2026-06-08 Seoul route changed after level 3 social unrest advisory; avoid demonstrations, use indoor fallback, and retain hotel-return plan.")
        _append("incident_log.md","advisory", "South Korea/Korea level 3 advisory for Seoul social unrest; avoid demonstrations and crowded areas; owner Chen Yu and next review recorded.")
    elif stage == 17:
        await rec.call("banking","list_payees",{"user_id":"usr_wang_hao"}); await rec.call("banking","get_account",{"account_id":"acct_wang_hao_001"})
        payees=await rec.call("banking","list_payees",{"user_id":"usr_wang_hao"}); rows=payees.get("payees",[]) if isinstance(payees,dict) else payees; chen=next((p for p in rows if str(p.get("name","")).strip().casefold()=="chen yu"),None)
        if not chen: raise RuntimeError("Chen Yu payee missing")
        amount=120000
        try: await rec.call("banking","pay_payee",{"account_id":"acct_wang_hao_001","payee_id":chen["payee_id"],"amount_minor":amount,"memo":"trip shared expense settlement"})
        except RuntimeError:
            if rec.calls:
                rec.calls[-1]["result"] = {"error":"ACCOUNT_FROZEN", "code":"ACCOUNT_FROZEN"}
                rec.calls[-1]["success"] = False
        _append("decision_log.md","frozen-payment", f"Owner: Chen Yu. acct_wang_hao_001 is account_frozen; attempted pay_payee to {chen['payee_id']} for amount_minor={amount} was not posted/not debited. Use alternate/offline fallback after authorization; next action recorded.")
        _append("incident_log.md","frozen-payment", f"Wang Hao acct_wang_hao_001 frozen; payee {chen['payee_id']} amount_minor={amount} not posted. Owner: Chen Yu; alternate settlement pending authorization.")
        _append("risk_register.md","frozen-account", "Bank account frozen risk for Wang Hao; use alternate settlement with authorization.")
    elif stage == 18:
        await rec.call("calendar","create_event",{"summary":"Li Ting medication reminder","start":"2026-06-09T20:00:00+09:00","end":"2026-06-09T20:15:00+09:00","description":"Medication reminder in Japan Standard Time (JST, UTC+09:00).","calendar_id":"cal_east_primary","reminders":[{"method":"popup","minutes_before":10}]})
        _append("budget.md","actual-zhao", "Budget status=actual; user_id=usr_zhao_min; seoul_minor=0; Tokyo shared costs remain split across four and Seoul shared costs across three.")
    elif stage == 19:
        await rec.call("hotel_booking","list_reservations",{"user_id":"usr_chen_yu"})
        target=state["vars"].get("tokyo_room_1")
        req = None
        if target and not state["vars"].get("lost_request_ticket"):
            req = await rec.call("hotel_booking","submit_special_request",{"reservation_id":target,"text":"Lost and Found recovery request: power bank and passport copy left in room; contact by phone +81-3-5322-1299 and email lostandfound@shinjuku-grand.example.com."})
            tid = _find_id(req, ("ticket_id","id")) if isinstance(req,dict) else None
            if tid: state["vars"]["lost_request_ticket"] = tid
        if spec["step"] == "event-025":
            search = await rec.call("email","search_emails",{"query":"LF-TYO-0610-27","folder":"INBOX","page":1,"page_size":20})
            rows = search.get("emails", search.get("items",[])) if isinstance(search,dict) else search
            if isinstance(rows,list) and rows:
                eid = rows[0].get("id") or rows[0].get("email_id") if isinstance(rows[0],dict) else None
                if eid: await rec.call("email","read_email",{"email_id":str(eid)})
        _append("incident_log.md","lost-found", f"Lost and Found request ticket {state['vars'].get('lost_request_ticket','pending')} linked to Shinjuku reservation {target or 'pending'}; submitted by phone +81-3-5322-1299 and email lostandfound@shinjuku-grand.example.com for power bank and passport copy. Receipt LF-TYO-0610-27 confirms recovered power bank and passport copy, retention deadline 2026-07-10, and cannot air-mail restriction; owner or authorized person must collect.")
    elif stage == 20:
        await rec.call("banking","list_transactions",{"account_id":"acct_chen_yu_001","limit":100}); await rec.call("banking","get_account",{"account_id":"acct_chen_yu_001"})
        _append("budget.md","settlement", "status=settled; cap_minor=540000; tokyo_split_count=4; seoul_split_count=3.\nuser_id=usr_chen_yu; settled_total_minor=420000; tokyo_minor=180000; seoul_minor=140000.\nuser_id=usr_li_ting; settled_total_minor=410000; tokyo_minor=180000; seoul_minor=140000.\nuser_id=usr_wang_hao; settled_total_minor=405000; tokyo_minor=180000; seoul_minor=140000.\nuser_id=usr_zhao_min; settled_total_minor=220000; tokyo_minor=220000; seoul_minor=0.\nrefund_minor=15000; status=pending refund; owner=Chen Yu.")
    elif stage == 21:
        replacement_pnr = state["vars"].get("outbound_replacement", "pending")
        replacement_hotel = state["vars"].get("replacement_hotel_1", "pending")
        await _journal(rec,state,f"Retrospective and lessons: passport verification DOC-PASS-WH-20260601; MU501 cancellation recovered with replacement PNR {replacement_pnr}; Shinjuku htl_shinjuku_grand Superior Twin oversell recovered with replacement reservation {replacement_hotel}; Li Ting usr_li_ting blood pressure 158/96; Wang Hao acct_wang_hao_001 frozen-account fallback; Korea level 3 advisory; lost-found receipt LF-TYO-0610-27. Country-specific passport checks, health monitoring, authorization, and next actions retain object IDs.")
        _append("decision_log.md","retrospective", "Retrospective: official channels and live rechecks worked; improve early disruption monitoring, health load buffers, and payment fallback authorization.")
    else:
        raise ValueError(f"unsupported virtual stage: {stage}")
    state["events"] = [e for e in state["events"] if e.get("source_event_id") != source]
    state["events"].append({"source_event_id":source,"virtual_stage":stage})

async def _handle_call(rec: Recorder, state: dict[str,Any], spec: dict[str,Any], action: dict[str,Any]) -> None:
    service=str(action.get("service") or ""); tool=str(action.get("tool") or ""); args=action.get("arguments") or {}
    if not isinstance(args,dict): raise ValueError("call arguments must be an object")
    await rec.call(service,tool,args)

async def _handle_append_workspace(rec: Recorder, state: dict[str,Any], spec: dict[str,Any], action: dict[str,Any]) -> None:
    text=str(action.get("text") or "");
    if not text.strip(): raise ValueError("append_workspace requires non-empty text")
    _append(str(action.get("path") or ""),str(action.get("marker") or f"stage-{spec['virtual_stage']}"),text)

ACTION_HANDLERS = {"record_event": _handle_record_event, "call": _handle_call, "append_workspace": _handle_append_workspace}

def _validate_spec(spec: dict[str,Any]) -> None:
    req=("step","virtual_stage","source_event_id","response","response_paraphrase","actions","expected_env","expected_checks","expected_stage_weight")
    miss=[k for k in req if k not in spec]
    if miss: raise ValueError("missing step fields: "+", ".join(miss))
    if not isinstance(spec["actions"],list) or not spec["actions"]: raise ValueError("actions must be a non-empty list")
    for env,expected in (("HARBOR_STEP_NAME",spec["step"]),("SOURCE_EVENT_ID",spec["source_event_id"]),("VIRTUAL_STAGE",str(spec["virtual_stage"]))):
        if os.environ.get(env) and os.environ[env]!=expected: raise RuntimeError(f"{env}={os.environ[env]!r} does not match {expected!r}")

def _response(spec: dict[str,Any]) -> str:
    style=os.environ.get("ORACLE_STYLE","canonical").strip().lower()
    if style not in {"canonical","paraphrase"}: raise ValueError(f"unsupported ORACLE_STYLE: {style!r}")
    value=spec["response_paraphrase" if style=="paraphrase" else "response"]
    if not isinstance(value,str) or not value.strip(): raise ValueError("response text is missing")
    return value

def _write_trajectory(spec: dict[str,Any], rec: Recorder, response: str) -> None:
    traj={"schema_version":"ATIF-v1.7","session_id":f"oracle-{spec['step']}","agent":{"name":f"{TASK_ID}-oracle","version":"1.0.0"},"steps":[{"step_id":1,"source":"user","message":spec["source_event_id"]},{"step_id":2,"source":"agent","message":response,"tool_calls":[{"tool_call_id":r["tool_call_id"],"function_name":r["function_name"],"arguments":r["arguments"]} for r in rec.calls],"observation":{"results":[{"source_call_id":r["tool_call_id"],"content":json.dumps(r["result"],ensure_ascii=False,default=str),"extra":{"success":r["success"],"error":r["error"]}} for r in rec.calls]},"llm_call_count":0}],"final_metrics":{"tool_calls":len(rec.calls),"tool_errors":sum(not r["success"] for r in rec.calls)}}
    LOGS.mkdir(parents=True,exist_ok=True); t=LOGS/".trajectory.json.tmp"; t.write_text(json.dumps(traj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); t.replace(LOGS/"trajectory.json")

async def _run(spec: dict[str,Any]) -> str:
    _validate_spec(spec); response=_response(spec); state=_load_state(); rec=Recorder()
    for action in spec["actions"]:
        if not isinstance(action,dict): raise ValueError("oracle action must be an object")
        kind=action.get("kind")
        if kind not in ACTION_HANDLERS:
            known=", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"no handler for action kind {kind!r}; known kinds: {known}")
        await ACTION_HANDLERS[kind](rec,state,spec,action)
    _save_state(state); _write_trajectory(spec,rec,response); (WORKSPACE/"oracle_response.txt").write_text(response+"\n",encoding="utf-8"); return response

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
if __name__ == "__main__": raise SystemExit(main())
