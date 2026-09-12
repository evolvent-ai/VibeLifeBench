"""Stage 15: authorized HKG transit booking — trace, backend segments, price, visa, persistence."""
from __future__ import annotations
from loguru import logger
from ._helpers import _agent_used_tool_with_args, _agent_used_tool, _workspace_file_text, _text_has_backend_flight_amounts, _booked_hkg_transit, _text_names_booked_hkg_flights, _agent_checked_transit_visa, _agent_booked_mct_violation, _agent_booked_tpe_transit


def s15_searched(env) -> bool:
    ok=_agent_used_tool_with_args(env,"flight_booking","search_flights",["nrt","hkg"],stage=15) and _agent_used_tool_with_args(env,"flight_booking","search_flights",["hkg","pvg"],stage=15)
    logger.info(f"s15_search: {ok}"); return ok


def s15_named(env) -> bool:
    text=_workspace_file_text(env,"/workspace/itinerary.md")
    ok=_booked_hkg_transit(env) and _text_names_booked_hkg_flights(env,text) and ("hkg" in text.lower() or "hong kong" in text.lower())
    logger.info(f"s15_named_backend: {ok}"); return ok


def s15_price(env) -> bool:
    text=_workspace_file_text(env,"/workspace/budget.md")
    ok=_booked_hkg_transit(env) and _text_has_backend_flight_amounts(env,text)
    logger.info(f"s15_price_backend: {ok}"); return ok


def s15_visa(env) -> bool:
    ok=_booked_hkg_transit(env) and _agent_checked_transit_visa(env)
    logger.info(f"s15_visa_formal: {ok}"); return ok


def s15_persisted(env) -> bool:
    text=_workspace_file_text(env,"/workspace/itinerary.md")+"\n"+_workspace_file_text(env,"/workspace/decision_log.md")
    created=_agent_used_tool(env,"flight_booking","create_booking",stage=15)
    ok=created and _booked_hkg_transit(env) and _text_names_booked_hkg_flights(env,text) and not _agent_booked_mct_violation(env) and not _agent_booked_tpe_transit(env)
    logger.info(f"s15_persist_backend: {ok}"); return ok


CHECKS=[("s15_searched",s15_searched,1.0),("s15_named",s15_named,1.0),("s15_price",s15_price,1.0),("s15_visa",s15_visa,1.0),("s15_persisted",s15_persisted,2.5)]
