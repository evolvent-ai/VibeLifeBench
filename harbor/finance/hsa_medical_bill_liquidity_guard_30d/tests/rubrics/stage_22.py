"""Stage 22 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_safety_critical, check_stage_crosslink


def s22_addressed(env) -> bool:
    return check_stage_addressed(env, 22)


def s22_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 22)


def s22_safety_critical(env) -> bool:
    return check_stage_safety_critical(env, 22)


def s22_crosslink(env) -> bool:
    return check_stage_crosslink(env, 22)


CHECKS = [
    ("s22_addressed", s22_addressed, 1.0),
    ("s22_tool_or_number", s22_tool_or_number, 2.0),
    ("s22_safety_critical", s22_safety_critical, 5.0),
    ("s22_crosslink", s22_crosslink, 3.0),
]
