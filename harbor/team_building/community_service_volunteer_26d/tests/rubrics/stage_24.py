from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s24_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 24)


def s24_durable_update(env) -> bool:
    return stage_durable_record(env, 24)


CHECKS = [
    ("s24_authority_trace", s24_authority_trace, 2.0),
    ("s24_durable_update", s24_durable_update, 0.25),
]
