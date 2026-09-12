"""Stage 15 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate


def s15_addressed(env) -> bool:
    return check_stage_addressed(env, 15)


def s15_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 15)


def s15_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 15)


CHECKS = [
    ("s15_addressed", s15_addressed, 1.0),
    ("s15_tool_or_number", s15_tool_or_number, 2.0),
    ("s15_durable_gate", s15_durable_gate, 5.0),
]
