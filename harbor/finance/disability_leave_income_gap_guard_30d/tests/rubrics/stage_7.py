"""Stage 7 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate


def s7_addressed(env) -> bool:
    return check_stage_addressed(env, 7)


def s7_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 7)


def s7_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 7)


CHECKS = [
    ("s7_addressed", s7_addressed, 1.0),
    ("s7_tool_or_number", s7_tool_or_number, 2.0),
    ("s7_durable_gate", s7_durable_gate, 5.0),
]
