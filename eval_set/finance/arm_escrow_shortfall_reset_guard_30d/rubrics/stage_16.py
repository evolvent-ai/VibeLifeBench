"""Stage 16 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s16_addressed(env) -> bool:
    return check_stage_addressed(env, 16)


def s16_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 16)


def s16_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 16)


def s16_crosslink(env) -> bool:
    return check_stage_crosslink(env, 16)


CHECKS = [
    ("s16_addressed", s16_addressed, 1.0),
    ("s16_tool_or_number", s16_tool_or_number, 2.0),
    ("s16_durable_gate", s16_durable_gate, 5.0),
    ("s16_crosslink", s16_crosslink, 3.0),
]
