"""Stage 9 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s9_addressed(env) -> bool:
    return check_stage_addressed(env, 9)


def s9_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 9)


def s9_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 9)


def s9_crosslink(env) -> bool:
    return check_stage_crosslink(env, 9)


CHECKS = [
    ("s9_addressed", s9_addressed, 1.0),
    ("s9_tool_or_number", s9_tool_or_number, 2.0),
    ("s9_durable_gate", s9_durable_gate, 5.0),
    ("s9_crosslink", s9_crosslink, 3.0),
]
