"""Stage 18 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate


def s18_addressed(env) -> bool:
    return check_stage_addressed(env, 18)


def s18_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 18)


def s18_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 18)


CHECKS = [
    ("s18_addressed", s18_addressed, 1.0),
    ("s18_tool_or_number", s18_tool_or_number, 2.0),
    ("s18_durable_gate", s18_durable_gate, 5.0),
]
