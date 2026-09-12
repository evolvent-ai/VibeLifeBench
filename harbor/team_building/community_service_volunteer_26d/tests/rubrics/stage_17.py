from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s17_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 17)


def s17_durable_update(env) -> bool:
    return stage_durable_record(env, 17)


CHECKS = [
    ("s17_authority_trace", s17_authority_trace, 2.0),
    ("s17_durable_update", s17_durable_update, 0.25),
]
