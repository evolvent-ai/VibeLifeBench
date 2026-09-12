from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s6_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 6)


def s6_durable_update(env) -> bool:
    return stage_durable_record(env, 6)


CHECKS = [
    ("s6_authority_trace", s6_authority_trace, 2.0),
    ("s6_durable_update", s6_durable_update, 0.25),
]
