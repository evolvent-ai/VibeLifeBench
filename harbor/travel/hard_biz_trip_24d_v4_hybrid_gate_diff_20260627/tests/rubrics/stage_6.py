"""Stage 6: booking hold - inventory reduction notice and status mutation."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _any, _stage_corpus, _agent_used_tool_with_args,
    _workspace_file_text,
)


def s6_checked_status(env) -> bool:
    """Agent checked flight/hotel status after mutation."""
    has_flight = _agent_used_tool_with_args(env, "flight_booking", "get_flight_status", ["mu523"], stage=6) or _agent_used_tool_with_args(env, "flight_booking", "get_flight_status", ["mu524"], stage=6)
    has_hotel = _agent_used_tool_with_args(env, "hotel_booking", "get_room_availability", ["hotel_roppongi_biz"], stage=6)
    ok = has_flight and has_hotel
    logger.info(f"s6_checked: flight={has_flight} hotel={has_hotel} -> {'PASS' if ok else 'FAIL'}")
    return ok


def s6_noted_inventory(env) -> bool:
    """Agent noted decreasing inventory and urgency."""
    text = (
        _stage_corpus(env, 6) + "\n" +
        _workspace_file_text(env, "/workspace/decision_log.md") + "\n" +
        _workspace_file_text(env, "/workspace/risk_register.md")
    ).lower()
    has_specific = _any(text, ["mu523", "mu524", "hotel_roppongi_biz", "roppongi business hotel"])
    has_deadline = _any(text, ["inventory", "decreasing", "cutoff", "deadline", "hold", "remaining", "limited", "cancellation deadline"])
    ok = s6_checked_status(env) and has_specific and has_deadline
    logger.info(f"s6_noted: specific={has_specific} deadline={has_deadline} -> {'PASS' if ok else 'FAIL'}")
    return ok


CHECKS = [
    ("s6_checked_status", s6_checked_status, 1.5),
    ("s6_noted_inventory", s6_noted_inventory, 1.0),
]
