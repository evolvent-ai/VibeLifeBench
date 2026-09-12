"""Stage 12: backend state and durable records prove the typhoon cancellations."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _agent_used_tool_with_args, _workspace_file_text, _typhoon_stage12_backend, _cancelled_direct_state, _refund_pending_backend


def _incident_text(env) -> str:
    return "\n".join(_workspace_file_text(env, p) for p in ["/workspace/incident_log.md", "/workspace/decision_log.md", "/workspace/risk_register.md", "/workspace/budget.md"]).lower()


def s12_reply_typhoon(env) -> bool:
    text=_incident_text(env); ok=_typhoon_stage12_backend(env) and _any(text,["typhoon","typhoon yinxing","yinxing"]) and _any(text,["cat 2","cat2","965","narita"])
    logger.info(f"s12_typhoon: {ok}"); return ok


def s12_reply_cancelled(env) -> bool:
    text=_incident_text(env); ok=_cancelled_direct_state(env) and _any(text,["cancelled","grounded","closed"]) and all(x in text for x in ["mu524","ca930","nh919"])
    logger.info(f"s12_cancel: {ok}"); return ok


def s12_reply_alternative(env) -> bool:
    text=_incident_text(env); ok=_cancelled_direct_state(env) and _any(text,["alternative","rebooking","transit","connection","option"]) and _any(text,["direct"]) and _any(text,["hkg","hong kong","icn","tpe","visa","mct","connection"])
    logger.info(f"s12_alt: {ok}"); return ok


def s12_tool_used(env) -> bool:
    ok=all(_agent_used_tool_with_args(env,"flight_booking","get_flight_status",[f.lower()],stage=12) for f in ["MU524","CA930","NH919"])
    logger.info(f"s12_tool: {ok}"); return ok


def s12_persisted(env) -> bool:
    text=_incident_text(env); described=all(x in text for x in ["mu524","ca930","nh919"]) and _any(text,["refund","pending","pending refund","not received"])
    ok=described and _cancelled_direct_state(env) and _refund_pending_backend(env)
    logger.info(f"s12_persist_backend: {ok}"); return ok


CHECKS=[("s12_reply_typhoon",s12_reply_typhoon,1.0),("s12_reply_cancelled",s12_reply_cancelled,1.0),("s12_reply_alternative",s12_reply_alternative,1.0),("s12_tool_used",s12_tool_used,1.0),("s12_persisted",s12_persisted,1.0)]
