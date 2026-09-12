from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s20_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 20)


def s20_durable_update(env) -> bool:
    return stage_durable_record(env, 20)


CHECKS = [
    ("s20_authority_trace", s20_authority_trace, 2.0),
    ("s20_durable_update", s20_durable_update, 0.25),
]
