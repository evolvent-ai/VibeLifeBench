"""Stage 8 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s8_addressed(env) -> bool:
    return check_stage_addressed(env, 8)


def s8_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 8)


def s8_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 8)


def s8_crosslink(env) -> bool:
    return check_stage_crosslink(env, 8)


CHECKS = [
    ("s8_addressed", s8_addressed, 1.0),
    ("s8_tool_or_number", s8_tool_or_number, 2.0),
    ("s8_durable_gate", s8_durable_gate, 5.0),
    ("s8_crosslink", s8_crosslink, 3.0),
]
