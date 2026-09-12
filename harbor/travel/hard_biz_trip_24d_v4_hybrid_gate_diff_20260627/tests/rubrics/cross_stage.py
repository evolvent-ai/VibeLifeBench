"""Cross-stage durable evidence and backend consistency checks."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _any, _workspace_file_text, _workspace_file_nonempty, _count_stages_with_tool,
    _agent_used_tool, _agent_used_tool_with_args, _agent_checked_transit_visa,
    _text_has_backend_flight_amounts, _text_has_backend_hotel_amounts,
    _booked_hkg_transit, _text_names_booked_hkg_flights, _typhoon_history_backend,
    _cancelled_direct_state, _refund_pending_backend, _bank_forex_state,
    _calendar_conflict_backend, _bank_reconciliation_state,
)


def cs_budget_nonempty(env) -> bool:
    ok=_workspace_file_nonempty(env,"/workspace/budget.md"); logger.info(f"cs_budget_nonempty: {ok}"); return ok


def cs_budget_currency(env) -> bool:
    t=_workspace_file_text(env,"/workspace/budget.md").lower(); ok=all(x in t for x in ["cny","jpy","hkd"]); logger.info(f"cs_budget_currency: {ok}"); return ok


def cs_meeting_constraint_reasoning(env) -> bool:
    text=(_workspace_file_text(env,"/workspace/decision_log.md")+_workspace_file_text(env,"/workspace/incident_log.md")).lower()
    used_email=_agent_used_tool(env,"email",stage=10); used_calendar=_agent_used_tool(env,"calendar",stage=10)
    described=_any(text,["7/20","july 20","2026-07-20"]) and _any(text,["14:00","2pm","2 pm"]) and _any(text,["conflict","overlap","keynote","keynote speech"]) and _any(text,["reschedule","alternative time","after the meeting","alternative"])
    ok=used_email and used_calendar and described and _calendar_conflict_backend(env); logger.info(f"cs_meeting_backend: {ok}"); return ok


def cs_budget_mid(env) -> bool:
    text=_workspace_file_text(env,"/workspace/budget.md")
    ok=_any(text,["typhoon","extended","additional","extra","adjusted","transit"]) and _booked_hkg_transit(env) and _text_names_booked_hkg_flights(env,text) and _text_has_backend_flight_amounts(env,text) and _text_has_backend_hotel_amounts(env,text)
    logger.info(f"cs_budget_mid: {ok}"); return ok


def cs_budget_final(env) -> bool:
    text=_workspace_file_text(env,"/workspace/budget.md").lower(); ok=_any(text,["final","reconciliation","settled","actual"]) and _any(text,["pending refund","pending","not received"]) and _refund_pending_backend(env) and _bank_reconciliation_state(env); logger.info(f"cs_budget_final: {ok}"); return ok


def cs_incident_nonempty(env) -> bool:
    ilog=_workspace_file_text(env,"/workspace/incident_log.md");risk=_workspace_file_text(env,"/workspace/risk_register.md");ok=len(ilog.strip())>80 and len(risk.strip())>80;logger.info(f"cs_incident_nonempty: {ok}");return ok


def cs_incident_typhoon(env) -> bool:
    c=_workspace_file_text(env,"/workspace/incident_log.md")+_workspace_file_text(env,"/workspace/risk_register.md");ok=_any(c,["typhoon","yinxing","typhoon yinxing"]) and _any(c,["cat 2","cat2","965"]) and _typhoon_history_backend(env);logger.info(f"cs_inc_typhoon_backend: {ok}");return ok


def cs_incident_transit(env) -> bool:
    c=_workspace_file_text(env,"/workspace/incident_log.md")+_workspace_file_text(env,"/workspace/risk_register.md");ok=_any(c,["connection","transit","hkg","hong kong","connecting itinerary"]) and _booked_hkg_transit(env) and _text_names_booked_hkg_flights(env,c);logger.info(f"cs_inc_transit_backend: {ok}");return ok


def cs_incident_refund(env) -> bool:
    c=_workspace_file_text(env,"/workspace/incident_log.md")+_workspace_file_text(env,"/workspace/risk_register.md");ok=_any(c,["ticket refund","refund","pending","claim"]) and "mu524" in c.lower() and _any(c,["not received","pending refund","3-5"]) and _refund_pending_backend(env);logger.info(f"cs_inc_refund_backend: {ok}");return ok


def cs_transit_searched(env) -> bool:
    ok=_agent_used_tool_with_args(env,"flight_booking","search_flights",["nrt","hkg"]) and _agent_used_tool_with_args(env,"flight_booking","search_flights",["hkg","pvg"]);logger.info(f"cs_transit_searched: {ok}");return ok


def cs_transit_visa(env) -> bool:
    text=_workspace_file_text(env,"/workspace/decision_log.md")+_workspace_file_text(env,"/workspace/itinerary.md");ok=_agent_checked_transit_visa(env) and _booked_hkg_transit(env) and _any(text,["hong kong","hkg"]) and _any(text,["visa","transit","visa-free"]);logger.info(f"cs_transit_visa: {ok}");return ok


def cs_transit_documented(env) -> bool:
    t=_workspace_file_text(env,"/workspace/itinerary.md")+_workspace_file_text(env,"/workspace/decision_log.md");ok=_booked_hkg_transit(env) and _text_names_booked_hkg_flights(env,t) and _any(t,["hkg","hong kong","connection","transit","connecting itinerary"]);logger.info(f"cs_transit_doc: {ok}");return ok


def cs_banking_monitored(env) -> bool:
    ok=_count_stages_with_tool(env,"banking")>=3;logger.info(f"cs_banking: {ok}");return ok


def cs_forex_detected(env) -> bool:
    text=_workspace_file_text(env,"/workspace/budget.md")+_workspace_file_text(env,"/workspace/evidence_log.md");ok=_bank_forex_state(env) and _any(text,["1.5%","ftf","foreign transaction","fee"]) and _any(text,["hong kong","hkg","200"]);logger.info(f"cs_forex_backend: {ok}");return ok


CHECKS=[
("cs_budget_nonempty",cs_budget_nonempty,1.0),("cs_budget_currency",cs_budget_currency,1.0),("cs_meeting_constraint_reasoning",cs_meeting_constraint_reasoning,0.5),("cs_budget_mid",cs_budget_mid,1.0),("cs_budget_final",cs_budget_final,1.0),("cs_incident_nonempty",cs_incident_nonempty,1.0),("cs_incident_typhoon",cs_incident_typhoon,1.0),("cs_incident_transit",cs_incident_transit,1.0),("cs_incident_refund",cs_incident_refund,1.0),("cs_transit_searched",cs_transit_searched,0.5),("cs_transit_visa",cs_transit_visa,2.0),("cs_transit_documented",cs_transit_documented,2.5),("cs_banking_monitored",cs_banking_monitored,1.0),("cs_forex_detected",cs_forex_detected,1.5)]
