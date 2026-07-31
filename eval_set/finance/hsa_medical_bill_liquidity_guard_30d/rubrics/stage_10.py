"""Stage 10 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s10_addressed(env) -> bool:
    return check_stage_addressed(env, 10)


def s10_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 10)


def s10_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 10)


def s10_crosslink(env) -> bool:
    return check_stage_crosslink(env, 10)


CHECKS = [
    ("s10_addressed", s10_addressed, 1.0),
    ("s10_tool_or_number", s10_tool_or_number, 2.0),
    ("s10_durable_gate", s10_durable_gate, 5.0),
    ("s10_crosslink", s10_crosslink, 3.0),
]
