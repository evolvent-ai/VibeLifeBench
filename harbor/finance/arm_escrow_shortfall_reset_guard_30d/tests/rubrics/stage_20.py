"""Stage 20 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s20_addressed(env) -> bool:
    return check_stage_addressed(env, 20)


def s20_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 20)


def s20_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 20)


def s20_crosslink(env) -> bool:
    return check_stage_crosslink(env, 20)


CHECKS = [
    ("s20_addressed", s20_addressed, 1.0),
    ("s20_tool_or_number", s20_tool_or_number, 2.0),
    ("s20_durable_gate", s20_durable_gate, 5.0),
    ("s20_crosslink", s20_crosslink, 3.0),
]
