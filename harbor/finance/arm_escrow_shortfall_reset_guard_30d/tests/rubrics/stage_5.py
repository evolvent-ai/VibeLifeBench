"""Stage 5 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s5_addressed(env) -> bool:
    return check_stage_addressed(env, 5)


def s5_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 5)


def s5_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 5)


def s5_crosslink(env) -> bool:
    return check_stage_crosslink(env, 5)


CHECKS = [
    ("s5_addressed", s5_addressed, 1.0),
    ("s5_tool_or_number", s5_tool_or_number, 2.0),
    ("s5_durable_gate", s5_durable_gate, 5.0),
    ("s5_crosslink", s5_crosslink, 3.0),
]
