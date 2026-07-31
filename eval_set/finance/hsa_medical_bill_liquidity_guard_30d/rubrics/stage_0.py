"""Stage 0 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s0_addressed(env) -> bool:
    return check_stage_addressed(env, 0)


def s0_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 0)


def s0_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 0)


def s0_crosslink(env) -> bool:
    return check_stage_crosslink(env, 0)


CHECKS = [
    ("s0_addressed", s0_addressed, 1.0),
    ("s0_tool_or_number", s0_tool_or_number, 2.0),
    ("s0_durable_gate", s0_durable_gate, 5.0),
    ("s0_crosslink", s0_crosslink, 3.0),
]
