"""Stage 7 checker — direct flights cancelled notification."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _tool_called_in_stage,
    _stage_text,
    _any,
)


def s7_responded_to_cancellation(env) -> bool:
    """Stage 7 called search_flights (actively seeking alternatives) AND response mentions transit/change/reroute."""
    ok_tools = _tool_called_in_stage(env, 7, ["search_flights"])
    text = _stage_text(env, 7)
    ok_text = _any(
        text,
        ["transit", "rebook", "search again", "alternative", "reroute", "connecting"],
    )
    ok = ok_tools and ok_text
    logger.info(f"s7_responded_to_cancellation: tools={ok_tools} text={ok_text} -> {ok}")
    return ok


CHECKS = [
    ("s7_responded_to_cancellation", s7_responded_to_cancellation, 1.25),
]
