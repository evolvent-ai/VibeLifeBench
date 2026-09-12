"""Stage 11 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s11_addressed(env) -> bool:
    return check_stage_addressed(env, 11)


def s11_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 11)


def s11_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 11)


def s11_crosslink(env) -> bool:
    return check_stage_crosslink(env, 11)


CHECKS = [
    ("s11_addressed", s11_addressed, 1.0),
    ("s11_tool_or_number", s11_tool_or_number, 2.0),
    ("s11_durable_gate", s11_durable_gate, 5.0),
    ("s11_crosslink", s11_crosslink, 3.0),
]
