from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s9_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 9)


def s9_durable_update(env) -> bool:
    return stage_durable_record(env, 9)


CHECKS = [
    ("s9_authority_trace", s9_authority_trace, 2.0),
    ("s9_durable_update", s9_durable_update, 0.25),
]
