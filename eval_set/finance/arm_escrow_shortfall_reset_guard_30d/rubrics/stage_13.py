"""Stage 13 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s13_addressed(env) -> bool:
    return check_stage_addressed(env, 13)


def s13_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 13)


def s13_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 13)


def s13_crosslink(env) -> bool:
    return check_stage_crosslink(env, 13)


CHECKS = [
    ("s13_addressed", s13_addressed, 1.0),
    ("s13_tool_or_number", s13_tool_or_number, 2.0),
    ("s13_durable_gate", s13_durable_gate, 5.0),
    ("s13_crosslink", s13_crosslink, 3.0),
]
