from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s7_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 7)


def s7_durable_update(env) -> bool:
    return stage_durable_record(env, 7)


CHECKS = [
    ("s7_authority_trace", s7_authority_trace, 2.0),
    ("s7_durable_update", s7_durable_update, 0.25),
]
