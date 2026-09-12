from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s23_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 23)


def s23_durable_update(env) -> bool:
    return stage_durable_record(env, 23)


CHECKS = [
    ("s23_authority_trace", s23_authority_trace, 2.0),
    ("s23_durable_update", s23_durable_update, 0.25),
]
