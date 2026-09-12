"""Stage 14 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate


def s14_addressed(env) -> bool:
    return check_stage_addressed(env, 14)


def s14_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 14)


def s14_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 14)


CHECKS = [
    ("s14_addressed", s14_addressed, 1.0),
    ("s14_tool_or_number", s14_tool_or_number, 2.0),
    ("s14_durable_gate", s14_durable_gate, 5.0),
]
