"""Stage 23 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s23_addressed(env) -> bool:
    return check_stage_addressed(env, 23)


def s23_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 23)


def s23_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 23)


def s23_crosslink(env) -> bool:
    return check_stage_crosslink(env, 23)


CHECKS = [
    ("s23_addressed", s23_addressed, 1.0),
    ("s23_tool_or_number", s23_tool_or_number, 2.0),
    ("s23_durable_gate", s23_durable_gate, 5.0),
    ("s23_crosslink", s23_crosslink, 3.0),
]
