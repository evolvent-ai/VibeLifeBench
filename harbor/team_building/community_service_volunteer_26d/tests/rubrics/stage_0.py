from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s0_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 0)


def s0_durable_update(env) -> bool:
    return stage_durable_record(env, 0)


CHECKS = [
    ("s0_authority_trace", s0_authority_trace, 2.0),
    ("s0_durable_update", s0_durable_update, 0.25),
]
