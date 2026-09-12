"""Stage 6 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s6_addressed(env) -> bool:
    return check_stage_addressed(env, 6)


def s6_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 6)


def s6_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 6)


def s6_crosslink(env) -> bool:
    return check_stage_crosslink(env, 6)


CHECKS = [
    ("s6_addressed", s6_addressed, 1.0),
    ("s6_tool_or_number", s6_tool_or_number, 2.0),
    ("s6_durable_gate", s6_durable_gate, 5.0),
    ("s6_crosslink", s6_crosslink, 3.0),
]
