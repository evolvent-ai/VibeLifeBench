"""Stage 1 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s1_addressed(env) -> bool:
    return check_stage_addressed(env, 1)


def s1_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 1)


def s1_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 1)


def s1_crosslink(env) -> bool:
    return check_stage_crosslink(env, 1)


CHECKS = [
    ("s1_addressed", s1_addressed, 1.0),
    ("s1_tool_or_number", s1_tool_or_number, 2.0),
    ("s1_durable_gate", s1_durable_gate, 5.0),
    ("s1_crosslink", s1_crosslink, 3.0),
]
