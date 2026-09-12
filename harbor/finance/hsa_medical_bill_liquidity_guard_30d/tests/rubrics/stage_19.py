"""Stage 19 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s19_addressed(env) -> bool:
    return check_stage_addressed(env, 19)


def s19_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 19)


def s19_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 19)


def s19_crosslink(env) -> bool:
    return check_stage_crosslink(env, 19)


CHECKS = [
    ("s19_addressed", s19_addressed, 1.0),
    ("s19_tool_or_number", s19_tool_or_number, 2.0),
    ("s19_durable_gate", s19_durable_gate, 5.0),
    ("s19_crosslink", s19_crosslink, 3.0),
]
