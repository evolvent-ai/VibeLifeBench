"""Stage 8: scheduled reminder - verify preparations two days before departure."""
from __future__ import annotations
from loguru import logger
from ._helpers import _any, _stage_corpus, _agent_used_tool_with_args, _workspace_file_text


def s8_acknowledged_reminder(env) -> bool:
    """Agent acknowledged the scheduled reminder and took action."""
    text = (
        _stage_corpus(env, 8) + "\n" +
        _workspace_file_text(env, "/workspace/decision_log.md") + "\n" +
        _workspace_file_text(env, "/workspace/risk_register.md")
    ).lower()
    checked_flight = _agent_used_tool_with_args(env, "flight_booking", "get_flight_status", ["mu523"], stage=8) or _agent_used_tool_with_args(env, "flight_booking", "get_flight_status", ["mu524"], stage=8)
    checked_hotel = _agent_used_tool_with_args(env, "hotel_booking", "get_room_availability", ["hotel_roppongi_biz"], stage=8)
    covered_items = all(_any(text, [kw]) for kw in ["cash", "approval"]) and _any(text, ["flight", "flight ticket"]) and _any(text, ["hotel", "accommodation"])
    ok = checked_flight and checked_hotel and covered_items
    logger.info(f"s8_ack: flight={checked_flight} hotel={checked_hotel} covered={covered_items} -> {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s8_acknowledged_reminder", s8_acknowledged_reminder, 1.5),
]
