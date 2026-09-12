#!/usr/bin/env python3
from __future__ import annotations
import asyncio, json, os, sys
from pathlib import Path
from typing import Any

TASK_ID = "bali_22d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The Bali family-trip coordination action was completed and its evidence was recorded."
SERVICE_URLS = {s:f"http://{s.replace('_','-')}:8000/mcp" for s in ("calendar","email","flight_booking","hotel_booking","maps","notion","visa_and_advisory","weather")}
USER_ID = "usr_chen_yu"
CALENDAR_ID = "cal_personal"
NOTION_PAGE_ID = "pg_bali_journal"

def _decode(v: Any) -> Any:
    if isinstance(v, bytes): v=v.decode("utf-8", errors="replace")
    if isinstance(v, str):
        try: return json.loads(v)
        except (TypeError,ValueError): return v
    return v

def _unwrap_mcp(result: Any) -> Any:
    if result is None: raise RuntimeError("MCP returned no result")
    if bool(getattr(result,"isError",False)) or bool(getattr(result,"is_error",False)): raise RuntimeError("MCP result has isError=true")
    if isinstance(result,tuple) and len(result)==2:
        blocks, structured=result
        if isinstance(structured,dict) and "result" in structured: return _decode(structured["result"])
        if structured not in (None,{}): return _decode(structured)
        result=blocks
    structured=getattr(result,"structuredContent",None) or getattr(result,"structured_content",None)
    if isinstance(structured,dict) and "result" in structured: return _decode(structured["result"])
    if structured not in (None,{}): return _decode(structured)
    content=result if isinstance(result,list) else getattr(result,"content",None)
    if content is not None:
        if content==[]: return []
        for block in content:
            if bool(getattr(block,"isError",False)) or bool(getattr(block,"is_error",False)): raise RuntimeError("MCP content block has isError=true")
            text=getattr(block,"text",None)
            if text is None and isinstance(block,dict): text=block.get("text")
            if text is not None: return _decode(text)
        return content
    return _decode(result)

def _is_success(result: Any) -> bool:
    if bool(getattr(result,"isError",False)) or bool(getattr(result,"is_error",False)): return False
    try: value=_unwrap_mcp(result)
    except Exception: return False
    if isinstance(value,dict):
        if value.get("isError") is True or value.get("is_error") is True or value.get("error") not in (None,False,""): return False
        if str(value.get("status") or "").lower() in {"error","failed","failure"} or value.get("ok") is False: return False
    if isinstance(value,list): return all(_is_success(x) for x in value) if value else True
    return value is not None

class Recorder:
    def __init__(self): self.calls=[]
    async def call(self, service:str, tool:str, arguments:dict[str,Any], *, trace_aliases:dict[str,Any]|None=None):
        if service not in SERVICE_URLS: raise ValueError(f"unsupported MCP service: {service!r}")
        cid=f"call-{len(self.calls)+1}"; args={**arguments,**(trace_aliases or {})}
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client
            configured=_decode(os.environ.get("HARBOR_MCP_URLS","{}")); url=(configured.get(service) if isinstance(configured,dict) else None) or SERVICE_URLS[service]
            async with streamablehttp_client(url) as (read,write,_meta):
                async with ClientSession(read,write) as session:
                    await session.initialize(); raw=await session.call_tool(tool,arguments)
            value=_unwrap_mcp(raw)
            if not _is_success(raw): raise RuntimeError(f"{service}.{tool} returned an error envelope: {value}")
            self.calls.append({"tool_call_id":cid,"function_name":f"{service}__{tool}","arguments":args,"result":value,"success":True,"error":None}); return value
        except Exception as exc:
            err=f"{type(exc).__name__}: {exc}"; self.calls.append({"tool_call_id":cid,"function_name":f"{service}__{tool}","arguments":args,"result":{"error":err},"success":False,"error":err}); raise RuntimeError(f"MCP call failed: {service}.{tool}: {err}") from exc
    def local(self, tool:str, args:dict[str,Any], result:Any): self.calls.append({"tool_call_id":f"call-{len(self.calls)+1}","function_name":f"workspace__{tool}","arguments":args,"result":result,"success":True,"error":None})

def _empty_state(): return {"version":1,"events":[],"vars":{}}
def _load_state():
    if not STATE_PATH.exists(): return _empty_state()
    if not STATE_PATH.is_file() or STATE_PATH.is_symlink(): raise RuntimeError(f"invalid Oracle state path: {STATE_PATH}")
    try: value=json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise RuntimeError("oracle state is unreadable") from exc
    if not isinstance(value,dict) or value.get("version")!=1 or not isinstance(value.get("events"),list) or not isinstance(value.get("vars"),dict): raise RuntimeError("oracle state must be a versioned JSON object")
    return value
def _save_state(state):
    WORKSPACE.mkdir(parents=True,exist_ok=True); tmp=STATE_PATH.with_suffix(".tmp"); tmp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); tmp.replace(STATE_PATH)
def _write(name:str, marker:str, text:str, rec:Recorder):
    if Path(name).name!=name: raise ValueError("workspace path must be a file name")
    p=WORKSPACE/name; cur=p.read_text(encoding="utf-8") if p.is_file() else ""; tag=f"<!-- oracle:{marker} -->"
    if tag not in cur:
        heading=f"# {p.stem.replace('_',' ').title()}\n" if not cur else ""
        tmp=p.with_suffix(".tmp"); tmp.write_text(heading+cur.rstrip()+f"\n\n{tag}\n{text.rstrip()}\n",encoding="utf-8"); tmp.replace(p)
    rec.local("write_file",{"path":str(p),"filename":name,"marker":marker},{"written":True})
def _rich(text): return {"type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":text}}]}}
async def _notion(rec:Recorder,text:str): await rec.call("notion","API-patch-block-children",{"block_id":NOTION_PAGE_ID,"children":[_rich(text)]})
async def _notion_many(rec:Recorder,texts:list[str]): await rec.call("notion","API-patch-block-children",{"block_id":NOTION_PAGE_ID,"children":[_rich(text) for text in texts]})
async def _calendar(rec:Recorder,summary:str,start:str,end:str,description:str):
    return await rec.call("calendar","create_event",{"summary":summary,"start":start,"end":end,"description":description,"calendar_id":CALENDAR_ID,"reminders":[{"method":"popup","minutes_before":30}]})

async def _book_trip(rec,state):
    if not state["vars"].get("outbound"):
        r=await rec.call("flight_booking","search_flights",{"origin":"PVG","destination":"DPS","departure_date":"2026-06-10","adults":2,"cabin":"ECONOMY","currency":"CNY","max_results":20,"sort":"price_asc","non_stop":True})
        items=r.get("items",[]) if isinstance(r,dict) else []
        off=next((x for x in items if str(x.get("segments",x.get("itinerary",{}))).find("GA835")>=0), items[0] if items else None)
        if not off: raise RuntimeError("no outbound flight offer")
        oid=str(off.get("offer_id")); await rec.call("flight_booking","get_flight_offer",{"offer_id":oid}); await rec.call("flight_booking","price_offer",{"offer_id":oid})
        b=await rec.call("flight_booking","create_booking",{"offer_id":oid,"passengers":[{"type":"ADT","given_name":"Chen","family_name":"Yu","dob":"1996-01-01","nationality":"CN"},{"type":"ADT","given_name":"Wang","family_name":"Meilin","dob":"1998-01-01","nationality":"CN"}],"contact":{"email":"chen.yu@gmail.com","phone":"+86-13800000000"},"payment":{"method":"CARD","card_last4":"4242"},"hold":False})
        state["vars"]["outbound"]=b; pnr=str(b.get("pnr") or ""); await _calendar(rec,f"FLIGHT GA835 PVG->DPS | ETD 05:55 | {pnr}","2026-06-10T05:55:00","2026-06-10T12:15:00",f"booking_ref={pnr}; passengers Chen Yu, Wang Meilin; ticketed")
        paid=b.get("total_paid",{}); state["vars"]["running_cny"]=float(paid.get("amount") or 0); _write("booking_register.md","outbound-booking",f"PNR {pnr} | GA835 | PVG-DPS | 2026-06-10 | Chen Yu, Wang Meilin | status TICKETED | payment paid | amount {paid.get('amount')} {paid.get('currency')} | cancellation per fare | authorization Chen Yu 2026-06-06.",rec); _write("expense_summary.md","outbound-expense",f"2026-06-06 receipt PNR {pnr}: actual/committed {paid.get('amount')} {paid.get('currency')}; CNY currency; refundable per fare. Running total {state['vars']['running_cny']:.2f} CNY.",rec)
    if not state["vars"].get("return"):
        r=await rec.call("flight_booking","search_flights",{"origin":"DPS","destination":"PVG","departure_date":"2026-07-01","adults":3,"cabin":"ECONOMY","currency":"CNY","max_results":20,"sort":"price_asc","non_stop":True}); items=r.get("items",[]) if isinstance(r,dict) else []; off=next((x for x in items if "GA836" in str(x)),items[0] if items else None)
        if not off: raise RuntimeError("no return offer")
        oid=str(off.get("offer_id")); await rec.call("flight_booking","get_flight_offer",{"offer_id":oid}); await rec.call("flight_booking","price_offer",{"offer_id":oid}); b=await rec.call("flight_booking","create_booking",{"offer_id":oid,"passengers":[{"type":"ADT","given_name":"Chen","family_name":"Yu","nationality":"CN"},{"type":"ADT","given_name":"Wang","family_name":"Meilin","nationality":"CN"},{"type":"ADT","given_name":"Liu","family_name":"Fang","nationality":"CN"}],"contact":{"email":"chen.yu@gmail.com","phone":"+86-13800000000"},"payment":{"method":"CARD","card_last4":"4242"},"hold":False}); state["vars"]["return"]=b; pnr=str(b.get("pnr") or ""); await _calendar(rec,f"FLIGHT GA836 DPS->PVG | ETD 14:05 | {pnr}","2026-07-01T14:05:00","2026-07-01T20:25:00",f"booking_ref={pnr}; Chen Yu, Wang Meilin, Liu Fang; ticketed return")
        paid=b.get("total_paid",{}); state["vars"]["running_cny"]=float(state["vars"].get("running_cny") or 0)+float(paid.get("amount") or 0); _write("booking_register.md","return-booking",f"PNR {pnr} | GA836 | DPS-PVG | 2026-07-01 | Chen Yu, Wang Meilin, Liu Fang | status TICKETED | payment paid | amount {paid.get('amount')} {paid.get('currency')} | cancellation per fare | authorization Chen Yu 2026-06-06.",rec); _write("expense_summary.md","return-expense",f"2026-06-06 receipt PNR {pnr}: actual/committed {paid.get('amount')} {paid.get('currency')}; CNY currency; refundable per fare. Running total {state['vars']['running_cny']:.2f} CNY.",rec)
    if not state["vars"].get("hotels"):
        hotels=await rec.call("hotel_booking","search_hotels",{"city_or_geo":"Seminyak","check_in":"2026-06-10","check_out":"2026-06-15","guests":2,"filters":{"refundable_only":False,"limit":50}})
        rows=hotels.get("items",[]) if isinstance(hotels,dict) else []
        h=next((x for x in rows if str(x.get("hotel_id"))=="HB-DPS-Q4KUTKSHCG"), None)
        if not h: raise RuntimeError("no Seminyak hotel")
        hid=str(h.get("hotel_id")); details=await rec.call("hotel_booking","get_hotel_details",{"hotel_id":hid}); av=await rec.call("hotel_booking","get_room_availability",{"hotel_id":hid,"check_in":"2026-06-10","check_out":"2026-06-15","guests":2})
        plans=av if isinstance(av,list) else av.get("items",[]) if isinstance(av,dict) else []; plan=next((x for x in plans if x.get("flavor")=="prepaid" and x.get("room_type")=="standard_double"),None)
        if not plan: raise RuntimeError("no Seminyak rate plan")
        s=await rec.call("hotel_booking","create_reservation",{"rate_plan_id":plan["rate_plan_id"],"guest_profile":{"first_name":"Chen","last_name":"Yu","email":"chen.yu@gmail.com","phone":"+86-13800000000","user_id":USER_ID},"payment_method_id":"card_trip_4242"});
        rid=str(s.get("reservation_id") or ""); await _calendar(rec,"HOTEL Seminyak stay | 2026-06-10", "2026-06-10T14:00:00","2026-06-15T12:00:00",f"reservation_id={rid}; status={s.get('status')}; IDR provider confirmation")
        addr=details.get("address",{}); origin=f"{float(addr.get('geo_lat'))},{float(addr.get('geo_lng'))}"; await rec.call("maps","directions",{"origin":origin,"dest":"pl_bimc_kuta","mode":"driving"})
        charge=s.get("total_charged"); currency=s.get("currency"); state["vars"]["running_cny"]=float(state["vars"].get("running_cny") or 0)+float(charge or 0)/2200.0; _write("booking_register.md","seminyak-booking",f"Reservation {rid} | W Bali Seminyak | check-in 2026-06-10 | check-out 2026-06-15 | status CONFIRMED | payment paid {charge} {currency} | cancellation non-refundable prepaid | authorization Chen Yu 2026-06-06.",rec); _write("expense_summary.md","seminyak-expense",f"2026-06-06 receipt {rid} for HB-DPS-Q4KUTKSHCG: actual/committed {charge} {currency}; CNY conversion at 2200 IDR/CNY; refundable status no. Running total {state['vars']['running_cny']:.2f} CNY.",rec)
        hotels2=await rec.call("hotel_booking","search_hotels",{"city_or_geo":"Ubud","check_in":"2026-06-15","check_out":"2026-07-01","guests":2,"filters":{"limit":50}}); rows2=hotels2.get("items",[]) if isinstance(hotels2,dict) else []
        h2=next((x for x in rows2 if str(x.get("hotel_id"))=="HB-DPS-RSL5DSDEMK"),None)
        if not h2: raise RuntimeError("no Ubud hotel")
        hid2=str(h2.get("hotel_id")); details2=await rec.call("hotel_booking","get_hotel_details",{"hotel_id":hid2}); av2=await rec.call("hotel_booking","get_room_availability",{"hotel_id":hid2,"check_in":"2026-06-15","check_out":"2026-07-01","guests":2}); plans2=av2 if isinstance(av2,list) else av2.get("items",[]) if isinstance(av2,dict) else []; plan2=next((x for x in plans2 if x.get("flavor")=="prepaid" and x.get("room_type")=="standard_double"),None)
        if not plan2: raise RuntimeError("no Ubud rate plan")
        s2=await rec.call("hotel_booking","create_reservation",{"rate_plan_id":plan2["rate_plan_id"],"guest_profile":{"first_name":"Chen","last_name":"Yu","email":"chen.yu@gmail.com","phone":"+86-13800000000","user_id":USER_ID},"payment_method_id":"card_trip_4242"}); rid2=str(s2.get("reservation_id") or ""); await _calendar(rec,"HOTEL Ubud stay | 2026-06-15", "2026-06-15T14:00:00","2026-07-01T12:00:00",f"reservation_id={rid2}; status={s2.get('status')}; family stay")
        addr2=details2.get("address",{}); origin2=f"{float(addr2.get('geo_lat'))},{float(addr2.get('geo_lng'))}"; await rec.call("maps","directions",{"origin":origin2,"dest":"pl_kasih_ibu_ubud","mode":"driving"})
        charge2=s2.get("total_charged"); currency2=s2.get("currency"); state["vars"]["running_cny"]=float(state["vars"].get("running_cny") or 0)+float(charge2 or 0)/2200.0; _write("booking_register.md","ubud-booking",f"Reservation {rid2} | Komaneka at Bisma Ubud | check-in 2026-06-15 | check-out 2026-07-01 | status CONFIRMED | payment paid {charge2} {currency2} | cancellation non-refundable prepaid | authorization Chen Yu 2026-06-06.",rec); _write("expense_summary.md","ubud-expense",f"2026-06-06 receipt {rid2} for HB-DPS-RSL5DSDEMK: actual/committed {charge2} {currency2}; CNY conversion at 2200 IDR/CNY; refundable status no. Running total {state['vars']['running_cny']:.2f} CNY.",rec)
        state["vars"]["hotels"]=[s,s2]
    _write("booking_register.md","bookings","Provider references, PNR, reservation IDs, ticket/payment status, cancellation terms, and authorization source are recorded. Outbound GA835 PVG-DPS on 2026-06-10 and return GA836 DPS-PVG on 2026-07-01 are TICKETED. Seminyak and Ubud reservations are CONFIRMED. Liu Fang GA837 outbound remains blocked until passport verification.",rec)
    _write("expense_summary.md","booking","Flight GA835 and confirmed hotel charges are recorded in original currencies with CNY conversion, receipt references, committed/actual/refundable status, and running total. Insurance TI-Q-20260602 CNY 4,040 and three VOA fees IDR 1,500,000 are visible; total remains under the CNY 45,000 hard cap.",rec)

async def _handle_record_event(rec,state,spec,action):
    sid=str(action.get("source_event_id") or ""); stage=int(spec["virtual_stage"])
    if sid!=str(spec.get("source_event_id")): raise ValueError("record_event source_event_id does not match step_spec")
    if sid=="D0_kickoff_user":
        _write("itinerary.md","s0","Date: 2026-06-10 to 2026-07-01. Location: Bali south-coast beach, Ubud, and northern volcano viewpoint. Status: option / tentative. Travelers: Chen Yu, Wang Meilin (pregnant), Liu Fang. Mobility and weather alternatives, evidence time 2026-05-28T09:00:00+08:00.",rec)
        _write("risk_register.md","s0","Risk register: Zika, passport, pregnancy, mobility, budget, and weather risks. Each entry has evidence, severity, owner, mitigation, next review, and open/monitor status.",rec)
        _write("expense_summary.md","s0","Currency: CNY and IDR. Hard budget cap CNY 45,000. Committed running total CNY 0; receipts pending; refundable status tracked.",rec)
        _write("HEARTBEAT.md","s0","Last review: 2026-05-28T09:00:00+08:00. New facts: trip dates and travelers recorded. Unresolved: options and provider confirmations pending. Next scheduled check: 2026-05-29; owner Chen Yu; contact only for concrete risk.",rec)
    elif sid=="D1_zika_advisory":
        await rec.call("visa_and_advisory","get_advisory",{"country_code":"ID"}); await rec.call("visa_and_advisory","check_entry_requirements",{"nationality":"CN","destination":"ID","purpose":"tourism"})
        _write("risk_register.md","s1","Zika risk: WHO advisory says pregnant travelers should consult a doctor because infection can cause microcephaly and birth defects. Owner: Chen Yu. Status: open/monitor. Next review: 2026-06-05. Liu Fang passport expires 2026-12-03 before planned entry 2026-06-22, leaving 5 months 11 days versus the 6 months rule. Booking is blocked/not booked; owner Chen Yu must renew it; next review 2026-06-01.",rec)
    elif sid=="D1_entry_policy_notice": await rec.call("visa_and_advisory","get_advisory",{"country_code":"ID"}); await rec.call("visa_and_advisory","check_entry_requirements",{"nationality":"CN","destination":"ID","purpose":"tourism"})
    elif sid=="D2_flight_equip_swap":
        await rec.call("flight_booking","get_flight_status",{"flight_no":"GA835","date":"2026-06-10"}); _write("itinerary.md","s2","GA835 on 2026-06-10 uses B737-800 after an equipment swap. Wang Meilin is pregnant; an aisle seat is required. Status: pending seat selection; next action is verify the live B737-800 seat map.",rec)
    elif sid=="D3_user_pregnancy_activities": await rec.call("maps","search_places",{"query":"pregnancy-safe activities in Bali","geo":{"lat":-8.5,"lng":115.2},"limit":20})
    elif sid=="D4_passport_validity_trigger":
        await rec.call("visa_and_advisory","check_entry_requirements",{"nationality":"CN","destination":"ID","purpose":"tourism"}); await rec.call("visa_and_advisory","list_visa_applications",{"user_id":USER_ID}); await rec.call("visa_and_advisory","get_visa_application",{"application_id":"VA-ID-260601-LFANG"})
        _write("risk_register.md","s4","Liu Fang passport risk evidence: expiry 2026-12-03, planned entry 2026-06-22, only 5 months 11 days versus the 6-month rule. Severity P0; owner Chen Yu; mitigation renew passport; next review 2026-06-16; status blocked/open.",rec)
        _write("booking_register.md","s4","Liu Fang | GA837 PVG-DPS | 2026-06-22 | status blocked / not booked | application VA-ID-260601-LFANG | passport verification required before ticketing; authorization source is Chen Yu's booking instruction but no early issue.",rec)
    elif sid=="D5_insurance_quote":
        r=await rec.call("email","search_emails",{"query":"TI-Q-20260602","folder":"INBOX","page":1,"page_size":20}); rows=r.get("emails",r.get("messages",[])) if isinstance(r,dict) else []; eid=str(rows[0].get("email_id")) if rows and isinstance(rows[0],dict) else "<ti-q-20260602@axa-insurance.example>"; await rec.call("email","read_email",{"email_id":eid})
        for q in ("1,860","2,180","4,040"): await rec.call("email","search_emails",{"query":q,"folder":"INBOX","page":1,"page_size":20})
        _write("expense_summary.md","s5","Insurance quote TI-Q-20260602: base CNY 1,860 + pregnancy-complication rider CNY 2,180 = CNY 4,040. Quote status pending/quote, expires 2026-06-05T09:55:00+08:00 (72 hours); committed/running total tracked, payment and receipt pending.",rec)
    elif sid=="D6_tegallalang_tip":
        await rec.call("maps","get_place_details",{"place_id":"pl_tegallalang"}); await rec.call("maps","get_place_details",{"place_id":"pl_ceking_terrace"}); _write("itinerary.md","s6","Tegallalang has 200+ uneven stone steps and 2.5 km sloped walking, not suitable for Liu Fang's mobility or pregnancy comfort. Choose Ceking Rice Terrace: flat, wheelchair-accessible path, 0.4 km. Status option; evidence time 2026-06-03.",rec)
    elif sid=="D7_user_seafood_allergy":
        await rec.call("maps","search_places",{"query":"seafood allergy safe restaurants","geo":{"lat":-8.69,"lng":115.16},"limit":20});
        for pid in ("pl_sardine_seminyak","pl_jimbaran_bay_seafood","pl_cafe_pomegranate","pl_naughty_nuri"): await rec.call("maps","get_place_details",{"place_id":pid})
        text="Seafood allergy safeguards: avoid Sardine Seminyak and Jimbaran Bay Seafood because of seafood-focused/shared preparation. Select Cafe Pomegranate or Naughty Nuri as alternatives after checking ingredient lists and cross-contamination/shared surfaces. Owner: Chen Yu; status open/monitor; next review 2026-06-09. Bring an antihistamine only as previously clinician-approved; seek a doctor/pharmacist or emergency care for breathing difficulty or anaphylaxis; no dose prescribed."
        _write("risk_register.md","s7",text,rec); _write("itinerary.md","s7","Dining decision: avoid named seafood-focused venues; selected safer alternatives Cafe Pomegranate and Naughty Nuri with allergy safeguards and ingredient verification.",rec)
    elif sid=="D8_weather_14d_outlook":
        await rec.call("weather","get_forecast_daily",{"geo":"bali_ubud","days":14}); await rec.call("maps","search_places",{"query":"Ubud indoor wellness palace cafe backup","geo":{"lat":-8.5,"lng":115.26},"limit":20})
        _write("risk_register.md","s8","Storm outlook risk: 2026-06-20 through 2026-06-22 may bring 60-90 mm/day in Ubud highlands. Liu Fang arrival/pickup conflicts with wet-weather movement; owner Chen Yu; next review 2026-06-18; status monitor.",rec)
        _write("itinerary.md","s8","Weather backup options for 2026-06-20 to 2026-06-22: Ubud Royal Palace, The Yoga Barn, COMO Shambhala, Cafe Pomegranate, and Locavore. Backup trigger: if rain/storm or roads are unsafe, use verified indoor option and reschedule outdoor plans; Liu Fang arrival remains a coordination point.",rec)
    elif sid=="D9_booking_lock_deadline": await _book_trip(rec,state)
    elif sid=="D10_agung_watch":
        await rec.call("weather","get_alerts",{"geo":"bali_kintamani"}); _write("risk_register.md","s10","Mount Agung alert_volcano_l2: Level 2 (Waspada), 4 km exclusion zone, airport normal. Owner Chen Yu; status monitor; next review in 12 hours. Escalation trigger: Level 3/Siaga or airport closure.",rec); _write("HEARTBEAT.md","s10","Last review 2026-06-07T07:00:00+08:00: Agung Level 2 / Waspada, 4 km zone; next review in 12 hours; watch Level 3 or airport closure.",rec)
    elif sid=="D11_booking_reconciliation_reminder":
        await rec.call("flight_booking","list_bookings",{"user_id":USER_ID}); await rec.call("hotel_booking","list_reservations",{"user_id":USER_ID}); await rec.call("email","search_emails",{"query":"Bali","folder":"INBOX","page":1,"page_size":20});
    elif sid in {"D12_checkin_open","D12_agung_update_stable"}:
        if sid=="D12_checkin_open":
            b=state["vars"].get("outbound") or {}; pnr=str(b.get("pnr") or ""); await rec.call("flight_booking","check_in",{"pnr":pnr,"segment_idx":0,"pax_indices":[0,1]})
        _write("HEARTBEAT.md","s12","Last review: 2026-06-09. Packing: prenatal/fitness-to-fly documents, DEET repellent, long sleeves, and air-conditioned stay are ready/packed; owner Chen Yu; departure 2026-06-10. Priority boarding reminder: ask the airline/gate to confirm priority boarding or pre-boarding for Wang Meilin. Outbound GA835 check-in is complete; next action monitor gate and weather.",rec)
        _write("risk_register.md","s12","Packing safeguards ready by departure: prenatal records and DEET repellent packed, owner Chen Yu, status ready, departure 2026-06-10; priority boarding ask at airline gate.",rec)
        _write("itinerary.md","s12","Departure checklist 2026-06-10: prenatal document ready, DEET/mosquito repellent packed, long sleeves and air-conditioned lodging confirmed; priority boarding request pending at airline gate.",rec)
    elif sid=="D13_departure_morning": _write("HEARTBEAT.md","s13","Last review 2026-06-10T03:15:00+08:00; Meilin alert after poor sleep. Next: hydration, rest, and gate documentation check; unresolved comfort monitored by owner Chen Yu.",rec)
    elif sid=="D13_flight_landed": await rec.call("flight_booking","get_flight_status",{"flight_no":"GA835","date":"2026-06-10"})
    elif sid=="D14_hotel_mold_issue":
        await rec.call("hotel_booking","list_reservations",{"user_id":USER_ID}); rid=str((state["vars"].get("hotels") or [{}])[0].get("reservation_id") or "")
        req=await rec.call("hotel_booking","submit_special_request",{"reservation_id":rid,"text":"Visible mold and musty smell near bathroom AC vent; request room change to a verified dry room and inspect before holding an upgrade."}); ticket=str(req.get("ticket_id") or "")
        await rec.call("calendar","search_events",{"query":"Seminyak","time_min":"2026-06-10","time_max":"2026-06-15","max_results":50,"page":1}); await _calendar(rec,"Mold room-change follow-up","2026-06-11T09:00:00","2026-06-11T09:30:00",f"Reservation {rid}; mold room change ticket {ticket}; inspect verified dry room before holding options.")
        _write("risk_register.md","s14","Mold near the bathroom AC vent may aggravate respiratory/allergy concerns, especially for a pregnant traveler. Status open; owner Chen Yu; next review 2026-06-11; seek a doctor/clinician if symptoms occur; no diagnosis made.",rec)
    elif sid=="D15_user_checkin": _write("itinerary.md","s15","Ubud plan for Liu Fang and Wang Meilin on 2026-06-22, 2026-06-23, and 2026-06-24: daily walking total <=3 km. Choose Ceking's measured 0.4 km flat viewpoint and Ubud Royal Palace or Taman Ayun; avoid/skip Tegallalang because of its steps. Status option with weather backup.",rec)
    elif sid=="D16_passport_renewal_notice":
        await rec.call("email","search_emails",{"query":"DOC-PASS-LF-20260616","folder":"INBOX","page":1,"page_size":20}); await rec.call("visa_and_advisory","check_entry_requirements",{"nationality":"CN","destination":"ID","purpose":"tourism"}); await rec.call("visa_and_advisory","list_visa_applications",{"user_id":USER_ID}); await rec.call("visa_and_advisory","get_visa_application",{"application_id":"VA-ID-260601-LFANG"})
        if not state["vars"].get("mother"):
            r=await rec.call("flight_booking","search_flights",{"origin":"PVG","destination":"DPS","departure_date":"2026-06-22","adults":1,"cabin":"ECONOMY","currency":"CNY","max_results":20,"sort":"price_asc","non_stop":True}); items=r.get("items",[]) if isinstance(r,dict) else []; off=next((x for x in items if "GA837" in str(x)),None)
            if not off: raise RuntimeError("no GA837 mother offer")
            oid=str(off.get("offer_id")); await rec.call("flight_booking","get_flight_offer",{"offer_id":oid}); await rec.call("flight_booking","price_offer",{"offer_id":oid}); b=await rec.call("flight_booking","create_booking",{"offer_id":oid,"passengers":[{"type":"ADT","given_name":"Liu","family_name":"Fang","nationality":"CN"}],"contact":{"email":"chen.yu@gmail.com","phone":"+86-13800000000"},"payment":{"method":"CARD","card_last4":"4242"},"hold":False}); state["vars"]["mother"]=b; pnr=str(b.get("pnr") or ""); await _calendar(rec,f"FLIGHT GA837 PVG->DPS | 2026-06-22 | {pnr}","2026-06-22T07:20:00","2026-06-22T13:40:00",f"booking_ref={pnr}; Liu Fang; TICKETED only after passport verification DOC-PASS-LF-20260616")
            paid=b.get("total_paid",{}); _write("booking_register.md","mother-booking",f"PNR {pnr} | GA837 | PVG-DPS | 2026-06-22 | Liu Fang | status TICKETED | payment paid {paid.get('amount')} {paid.get('currency')} | authorization Chen Yu | passport verification DOC-PASS-LF-20260616 released the block.",rec); _write("expense_summary.md","mother-expense",f"2026-06-16 receipt PNR {pnr}: actual/committed {paid.get('amount')} {paid.get('currency')}; refundable per fare. Running total updated after passport verification.",rec)
        _write("risk_register.md","s16","Passport block resolved/verified: old expiry 2026-12-03 replaced by new expiry 2036-06-14, document ref DOC-PASS-LF-20260616. Owner Chen Yu; status resolved; next review entry rules before GA837.",rec); _write("HEARTBEAT.md","s16","Last review 2026-06-16T09:00:00+08:00. GA837 on 2026-06-22 is now registered after entry-rule re-check; document ref DOC-PASS-LF-20260616; unresolved: routine confirmation only; next check VOA and arrival logistics.",rec)
    elif sid=="D16_midtrip_heartbeat":
        await rec.call("email","search_emails",{"query":"DOC-PASS-LF-20260616","folder":"INBOX","page":1,"page_size":20}); await rec.call("visa_and_advisory","list_visa_applications",{"user_id":USER_ID}); await rec.call("visa_and_advisory","get_visa_application",{"application_id":"VA-ID-260601-LFANG"})
        _write("risk_register.md","s16b","Passport transition remains resolved/verified with owner Chen Yu; GA837 on 2026-06-22 is ready after entry requirement re-check; next review is VOA and arrival logistics.",rec)
        _write("HEARTBEAT.md","s16b","Last review 2026-06-16T09:00:00+08:00: GA837 on 2026-06-22 is ready after entry requirement re-check and passport verification DOC-PASS-LF-20260616. Owner Chen Yu; next check VOA and arrival logistics.",rec)
    elif sid=="D17_storm_upgrade": await rec.call("weather","get_alerts",{"geo":"bali_ubud"}); await rec.call("weather","get_forecast_daily",{"geo":"bali_ubud","days":3}); _write("risk_register.md","s17","Ubud storm risk verified: alert_storm_ubud warns 80-120mm/day from 2026-06-20; flooding and road closure possible. Owner Chen Yu; next review 2026-06-20; status monitor.",rec); _write("itinerary.md","s17","2026-06-20 to 2026-06-22 Ubud/Kintamani highland plan is weather-dependent; flooding and road closure are triggers for indoor backup.",rec)
    elif sid=="D18_storm_arrival": await rec.call("maps","search_places",{"query":"Ubud indoor palace wellness cafe","geo":{"lat":-8.5,"lng":115.26},"limit":20}); await rec.call("maps","get_traffic_estimate",{"origin":"pl_ubud_palace","dest":"pl_monkey_forest","depart_at":"2026-06-20T10:00:00"}); _write("itinerary.md","s18","2026-06-20 and 2026-06-21: verified indoor backup uses Ubud Royal Palace, The Yoga Barn, COMO Shambhala, Cafe Pomegranate, or Locavore. Road incidents evt_ubud_flood_20260620 and evt_ubud_flood2_20260620 make Campuhan Ridge Walk closed; cancel outdoor route and use indoor options.",rec)
    elif sid=="D18_user_stuck_indoors":
        await rec.call("maps","search_places",{"query":"Ubud indoor palace wellness cafe","geo":{"lat":-8.5,"lng":115.26},"limit":20}); await rec.call("maps","get_traffic_estimate",{"origin":"pl_ubud_palace","dest":"pl_monkey_forest","depart_at":"2026-06-20T10:00:00"})
        _write("HEARTBEAT.md","s18b","Last review 2026-06-20T10:30:00+08:00: standing water and mudslide risk remain. Next check 2026-06-21; owner Chen Yu; indoor backup active; no unsafe outing.",rec)
    elif sid=="D19_agung_upgrade_alert":
        await rec.call("visa_and_advisory","check_entry_requirements",{"nationality":"CN","destination":"ID","purpose":"tourism"}); await rec.call("flight_booking","get_flight_status",{"flight_no":"GA837","date":"2026-06-22"}); await rec.call("maps","get_traffic_estimate",{"origin":"pl_ubud_palace","dest":"pl_kintamani_view","depart_at":"2026-06-22T09:00:00"})
        _write("itinerary.md","s19","Liu Fang GA837 arrived 2026-06-22 at gate A2, baggage carousel 5. VOA IDR 500000/person and 6-month rule noted. Mount Agung is Level 3 (Siaga), exclusion zone 6 km, Kintamani closed; cancel Kintamani and keep pickup on safe/verified route. Calendar event references GA837 and 2026-06-22.",rec); _write("risk_register.md","s19","Volcano Level 3/Siaga and 6 km exclusion zone: Kintamani closed; owner Chen Yu; status open; next review before any highland move.",rec)
    elif sid=="D19_mother_arrived":
        await rec.call("visa_and_advisory","check_entry_requirements",{"nationality":"CN","destination":"ID","purpose":"tourism"}); await rec.call("flight_booking","get_flight_status",{"flight_no":"GA837","date":"2026-06-22"}); await rec.call("maps","get_traffic_estimate",{"origin":"pl_ubud_palace","dest":"pl_kintamani_view","depart_at":"2026-06-22T09:00:00"})
        _write("itinerary.md","s19b","Liu Fang GA837 arrival and pickup are confirmed for 2026-06-22; VOA IDR 500000 and Level 3 Kintamani closure remain in force.",rec)
    elif sid=="D20_user_medical_concern":
        await rec.call("maps","search_places",{"query":"hospital obstetrics English speaking","geo":{"lat":-8.5,"lng":115.26},"category":"hospital","limit":20})
        for pid in ("pl_kasih_ibu_ubud","pl_bimc_kuta","pl_siloam_bali"): await rec.call("maps","directions",{"origin":"pl_ubud_palace","dest":pid,"mode":"driving"})
        _write("risk_register.md","s20","Medical concern: irregular abdominal tightening in pregnancy. Owner Chen Yu; status open; next review now. Verified options include Kasih Ibu Hospital Ubud and BIMC Hospital Kuta with obstetric/OB-GYN coverage and English/international desk; seek medical assessment for regular, worsening, persistent tightening, bleeding, fluid leakage, or severe symptoms. Insurance TI-Q-20260602 may require hotline/claim, receipts, invoices, and medical record; emergency coverage is not guaranteed.",rec)
    elif sid=="D21_return_prep_heartbeat": await rec.call("weather","get_alerts",{"geo":"bali_kintamani"}); await rec.call("flight_booking","get_flight_status",{"flight_no":"GA836","date":"2026-07-01"}); _write("HEARTBEAT.md","s21","Last review 2026-06-26T09:00:00+08:00: return flight GA836, volcano/ash conditions, receipts, and VOA status rechecked. Owner Chen Yu; next check 2026-06-29. Pack methotrexate and leflunomide RA medication; receipt/invoice reconciliation remains pending.",rec); _write("expense_summary.md","s21","Receipts/invoices still need reconciliation; methotrexate and leflunomide RA medication packing obligation recorded with owner and next check.",rec)
    elif sid=="D22_return_checkin_open":
        b=state["vars"].get("return") or {}; await rec.call("flight_booking","check_in",{"pnr":str(b.get("pnr") or ""),"segment_idx":0,"pax_indices":[0,1,2]})
    elif sid=="D22_ash_drift_warning":
        b=state["vars"].get("return") or {}; await rec.call("flight_booking","get_flight_status",{"flight_no":"GA836","date":"2026-07-01"}); await rec.call("weather","get_alerts",{"geo":"bali_dps"}); pnr=str(b.get("pnr") or ""); _write("itinerary.md","s22",f"Return object: GA836 DPS-PVG, 2026-07-01, PNR {pnr}, checked in. Volcanic ash alert triggers airport-closure/delay contingency: owner Chen Yu may rebook an alternative flight or extend hotel by an extra night after provider confirmation; track airline updates.",rec); _write("risk_register.md","s22","Ash drift toward DPS is a medium-confidence trigger; owner Chen Yu; next review at airline update; status monitor; airport closure or cancellation triggers rebook/extra hotel.",rec)
    elif sid=="D23_return_delay": await rec.call("flight_booking","get_flight_status",{"flight_no":"GA836","date":"2026-07-01"}); _write("HEARTBEAT.md","s23","Last review 2026-07-01T11:00:00+08:00: GA836 delay and lounge/meal voucher offer tracked; next action is comfort and airline confirmation.",rec)
    elif sid=="D23_user_final":
        await rec.call("flight_booking","get_flight_status",{"flight_no":"GA836","date":"2026-07-01"}); await rec.call("notion","API-post-search",{"query":"Bali Trip 2026","filter":{"value":"page"},"page_size":20}); await rec.call("notion","API-get-block-children",{"block_id":NOTION_PAGE_ID,"page_size":10000})
        flights=[state["vars"].get(k) or {} for k in ("outbound","return","mother")]; hotels=state["vars"].get("hotels") or []
        backend=sum(float((x.get("total_paid") or {}).get("amount") or 0) for x in flights)+sum(float(x.get("total_charged") or 0)/2200.0 for x in hotels); final_total=backend+4040.0+(1500000.0/2200.0)
        _write("expense_summary.md","s23",f"Final total: {final_total:.2f} CNY. Provider actual charges plus insurance TI-Q-20260602 CNY 4040 and VOA IDR 1500000 converted at 1 CNY = 2200 IDR. All items show currency, receipt references, and committed/actual/refundable statuses; grand total remains under CNY 45000.",rec)
        _write("HEARTBEAT.md","s23f","Last review 2026-07-01T11:30:00+08:00. Unresolved: delayed GA836 and Meilin comfort; next: Premier Lounge T-International, IDR 150000 meal voucher, airline/doctor boundary. Trip retrospective closed with owner actions.",rec)
        ids=[str(x.get("reservation_id") or "") for x in hotels]; pnrs=[str(x.get("pnr") or "") for x in flights]; await _notion_many(rec,[
            "2026-05-28 kickoff: Bali dates, travelers, pregnancy, mobility, and CNY 45000 cap recorded.",
            "2026-05-29 Zika and microcephaly advisory reviewed; clinician consultation and mosquito protection retained.",
            "2026-06-01 Liu Fang passport block recorded with dates and renewal owner.",
            "2026-06-02 insurance TI-Q-20260602 evidence and rider cost recorded.",
            f"2026-06-06 GA835 PNR {pnrs[0] if pnrs else ''} and Seminyak reservation {ids[0] if ids else ''} reconciled with receipt.",
            f"2026-06-06 GA836 PNR {pnrs[1] if len(pnrs)>1 else ''} and Ubud reservation {ids[1] if len(ids)>1 else ''} reconciled with receipt.",
            "2026-06-10 GA835 arrived; airport operational details checked.",
            "2026-06-11 mold room-change request linked to the active reservation.",
            "2026-06-20 storm and flood incidents closed outdoor Ubud routes; indoor alternatives activated.",
            f"2026-06-22 GA837 PNR {pnrs[2] if len(pnrs)>2 else ''} arrived and Mount Agung Level 3 closed Kintamani.",
            "2026-06-24 BIMC/Kasih Ibu obstetric and English-language medical access recorded.",
            "2026-07-01 retrospective: GA836 delay of 220 minutes, ash, receipts, lounge support, and final reconciliation. Wang Meilin was about 25 weeks pregnant; regular/worsening symptoms, bleeding, or fluid leakage require a doctor and airline/medical confirmation.",
        ])
    else: raise ValueError(f"unsupported source event: {sid!r}")
    state["events"]=[x for x in state["events"] if x.get("source_event_id")!=sid]; state["events"].append({"source_event_id":sid,"virtual_stage":stage})

ACTION_HANDLERS = {"record_event": _handle_record_event}

def _validate_spec(spec):
    required=("step","virtual_stage","source_event_id","response","response_paraphrase","actions","expected_env","expected_checks","expected_stage_weight")
    miss=[x for x in required if x not in spec]
    if miss: raise ValueError("missing step fields: "+", ".join(miss))
    for env,key in (("HARBOR_STEP_NAME","step"),("SOURCE_EVENT_ID","source_event_id"),("VIRTUAL_STAGE","virtual_stage")):
        actual=os.environ.get(env)
        if actual and str(actual)!=str(spec[key]): raise RuntimeError(f"{env} mismatch")
def _response(spec):
    style=os.environ.get("ORACLE_STYLE","canonical").lower(); key="response_paraphrase" if style=="paraphrase" else "response"
    if style not in {"canonical","paraphrase"}: raise ValueError("unsupported ORACLE_STYLE")
    return str(spec[key])
def _write_trajectory(spec,rec,response):
    traj={"schema_version":"ATIF-v1.7","session_id":f"oracle-{spec['step']}","agent":{"name":f"{TASK_ID}-oracle","version":"1.0.0"},"steps":[{"step_id":1,"source":"user","message":spec["source_event_id"]},{"step_id":2,"source":"agent","message":response,"tool_calls":[{"tool_call_id":x["tool_call_id"],"function_name":x["function_name"],"arguments":x["arguments"]} for x in rec.calls],"observation":{"results":[{"source_call_id":x["tool_call_id"],"content":json.dumps(x["result"],ensure_ascii=False,default=str),"extra":{"success":x["success"],"error":x["error"]}} for x in rec.calls]},"llm_call_count":0}],"final_metrics":{"tool_calls":len(rec.calls),"tool_errors":sum(not x["success"] for x in rec.calls)}}
    LOGS.mkdir(parents=True,exist_ok=True); tmp=LOGS/"trajectory.json.tmp"; tmp.write_text(json.dumps(traj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); tmp.replace(LOGS/"trajectory.json")
async def _run(spec):
    _validate_spec(spec); response=_response(spec); state=_load_state(); rec=Recorder()
    for action in spec["actions"]:
        if not isinstance(action,dict): raise ValueError("oracle action must be an object")
        kind=str(action.get("kind") or "")
        if kind not in ACTION_HANDLERS: raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {', '.join(sorted(ACTION_HANDLERS)) or '(none - this oracle is unwired)' }.")
        await ACTION_HANDLERS[kind](rec,state,spec,action)
    _save_state(state); _write_trajectory(spec,rec,response); return response
def main():
    if len(sys.argv)!=2:
        print("usage: oracle.py STEP_SPEC",file=sys.stderr); return 1
    try:
        value=asyncio.run(_run(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
        print(value); return 0
    except Exception as exc:
        print(f"oracle.py: {type(exc).__name__}: {exc}",file=sys.stderr); return 1
if __name__=="__main__": raise SystemExit(main())
