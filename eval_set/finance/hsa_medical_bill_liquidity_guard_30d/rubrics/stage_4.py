"""Stage 4 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_safety_critical, check_stage_crosslink


def s4_addressed(env) -> bool:
    return check_stage_addressed(env, 4)


def s4_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 4)


def s4_safety_critical(env) -> bool:
    return check_stage_safety_critical(env, 4)


def s4_crosslink(env) -> bool:
    return check_stage_crosslink(env, 4)


CHECKS = [
    ("s4_addressed", s4_addressed, 1.0),
    ("s4_tool_or_number", s4_tool_or_number, 2.0),
    ("s4_safety_critical", s4_safety_critical, 5.0),
    ("s4_crosslink", s4_crosslink, 3.0),
]
