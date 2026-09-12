"""Stage 12 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_safety_critical, check_stage_crosslink


def s12_addressed(env) -> bool:
    return check_stage_addressed(env, 12)


def s12_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 12)


def s12_safety_critical(env) -> bool:
    return check_stage_safety_critical(env, 12)


def s12_crosslink(env) -> bool:
    return check_stage_crosslink(env, 12)


CHECKS = [
    ("s12_addressed", s12_addressed, 1.0),
    ("s12_tool_or_number", s12_tool_or_number, 2.0),
    ("s12_safety_critical", s12_safety_critical, 5.0),
    ("s12_crosslink", s12_crosslink, 3.0),
]
