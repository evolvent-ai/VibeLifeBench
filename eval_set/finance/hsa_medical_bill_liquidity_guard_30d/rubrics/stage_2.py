"""Stage 2 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s2_addressed(env) -> bool:
    return check_stage_addressed(env, 2)


def s2_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 2)


def s2_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 2)


def s2_crosslink(env) -> bool:
    return check_stage_crosslink(env, 2)


CHECKS = [
    ("s2_addressed", s2_addressed, 1.0),
    ("s2_tool_or_number", s2_tool_or_number, 2.0),
    ("s2_durable_gate", s2_durable_gate, 5.0),
    ("s2_crosslink", s2_crosslink, 3.0),
]
