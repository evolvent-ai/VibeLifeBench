from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s16_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 16)


def s16_durable_update(env) -> bool:
    return stage_durable_record(env, 16)


CHECKS = [
    ("s16_authority_trace", s16_authority_trace, 2.0),
    ("s16_durable_update", s16_durable_update, 0.25),
]
