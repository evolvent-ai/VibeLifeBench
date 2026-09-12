from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s21_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 21)


def s21_durable_update(env) -> bool:
    return stage_durable_record(env, 21)


CHECKS = [
    ("s21_authority_trace", s21_authority_trace, 2.0),
    ("s21_durable_update", s21_durable_update, 0.25),
]
