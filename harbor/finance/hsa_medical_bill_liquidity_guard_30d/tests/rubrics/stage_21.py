"""Stage 21 rubric."""
from __future__ import annotations

from .stage_checks import check_stage_addressed, check_stage_tool_or_number, check_stage_durable_gate, check_stage_crosslink


def s21_addressed(env) -> bool:
    return check_stage_addressed(env, 21)


def s21_tool_or_number(env) -> bool:
    return check_stage_tool_or_number(env, 21)


def s21_durable_gate(env) -> bool:
    return check_stage_durable_gate(env, 21)


def s21_crosslink(env) -> bool:
    return check_stage_crosslink(env, 21)


CHECKS = [
    ("s21_addressed", s21_addressed, 1.0),
    ("s21_tool_or_number", s21_tool_or_number, 2.0),
    ("s21_durable_gate", s21_durable_gate, 5.0),
    ("s21_crosslink", s21_crosslink, 3.0),
]
