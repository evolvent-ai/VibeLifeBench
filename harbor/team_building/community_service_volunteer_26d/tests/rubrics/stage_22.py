from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s22_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 22)


def s22_durable_update(env) -> bool:
    return stage_durable_record(env, 22)


CHECKS = [
    ("s22_authority_trace", s22_authority_trace, 2.0),
    ("s22_durable_update", s22_durable_update, 0.25),
]
