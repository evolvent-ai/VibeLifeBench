from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s14_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 14)


def s14_durable_update(env) -> bool:
    return stage_durable_record(env, 14)


CHECKS = [
    ("s14_authority_trace", s14_authority_trace, 2.0),
    ("s14_durable_update", s14_durable_update, 0.25),
]
