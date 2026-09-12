from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s1_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 1)


def s1_durable_update(env) -> bool:
    return stage_durable_record(env, 1)


CHECKS = [
    ("s1_authority_trace", s1_authority_trace, 2.0),
    ("s1_durable_update", s1_durable_update, 0.25),
]
