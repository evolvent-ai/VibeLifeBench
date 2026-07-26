"""Stage 17 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s17_addressed(env) -> bool:
    return check_stage_addressed(env, 17)


def s17_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 17)


def s17_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 17)


def s17_crosslink(env) -> bool:
    return check_stage_crosslink(env, 17)


CHECKS = [
    ("s17_addressed", s17_addressed, 1.0),
    ("s17_tool_or_number", s17_tool_or_number, 2.0),
    ("s17_durable_gate", s17_durable_gate, 5.0),
    ("s17_crosslink", s17_crosslink, 3.0),
]
