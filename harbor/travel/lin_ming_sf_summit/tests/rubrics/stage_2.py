"""Stage 2 checker — user asks flight + hotel."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _tool_called_in_stage,
    _stage_text,
    _any,
)


def s2_searched_with_health(env) -> bool:
    """Stage 2 has search_flights AND search_hotels AND get_health_restrictions, AND response shows constraint awareness."""
    ok_flights = _tool_called_in_stage(env, 2, ["search_flights"])
    ok_hotels = _tool_called_in_stage(env, 2, ["search_hotels"])
    tool_health = _tool_called_in_stage(env, 2, ["list_health_alerts", "get_goals", "get_goal_progress"])  # real health_tracker tools (was phantom get_health_restrictions)
    text = _stage_text(env, 2)
    text_ok = _any(
        text,
        ["lumbar spine", "business class", "business", "transit", "stopover", "connecting", "10 hours", "ten hours", "health"],
    )
    ok = ok_flights and ok_hotels and tool_health and text_ok
    logger.info(f"s2_searched_with_health: flights={ok_flights} hotels={ok_hotels} health_tool={tool_health} health_text={text_ok} -> {ok}")
    return ok


CHECKS = [
    ("s2_searched_with_health", s2_searched_with_health, 1.25),
]
