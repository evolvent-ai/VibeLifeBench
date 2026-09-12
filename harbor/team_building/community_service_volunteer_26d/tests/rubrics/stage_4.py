from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s4_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 4)


def s4_durable_update(env) -> bool:
    return stage_durable_record(env, 4)


CHECKS = [
    ("s4_authority_trace", s4_authority_trace, 2.0),
    ("s4_durable_update", s4_durable_update, 0.25),
]
