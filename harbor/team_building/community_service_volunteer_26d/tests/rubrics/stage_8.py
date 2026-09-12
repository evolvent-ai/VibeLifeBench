from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s8_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 8)


def s8_durable_update(env) -> bool:
    return stage_durable_record(env, 8)


CHECKS = [
    ("s8_authority_trace", s8_authority_trace, 2.0),
    ("s8_durable_update", s8_durable_update, 0.25),
]
