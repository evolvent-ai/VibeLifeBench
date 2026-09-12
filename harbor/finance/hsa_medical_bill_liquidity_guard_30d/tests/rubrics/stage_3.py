"""Stage 3 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s3_addressed(env) -> bool:
    return check_stage_addressed(env, 3)


def s3_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 3)


def s3_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 3)


def s3_crosslink(env) -> bool:
    return check_stage_crosslink(env, 3)


CHECKS = [
    ("s3_addressed", s3_addressed, 1.0),
    ("s3_tool_or_number", s3_tool_or_number, 2.0),
    ("s3_durable_gate", s3_durable_gate, 5.0),
    ("s3_crosslink", s3_crosslink, 3.0),
]
