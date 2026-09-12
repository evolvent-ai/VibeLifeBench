from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s2_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 2)


def s2_durable_update(env) -> bool:
    return stage_durable_record(env, 2)


CHECKS = [
    ("s2_authority_trace", s2_authority_trace, 2.0),
    ("s2_durable_update", s2_durable_update, 0.25),
]
