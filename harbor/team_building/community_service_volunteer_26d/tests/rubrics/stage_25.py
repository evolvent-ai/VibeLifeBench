from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s25_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 25)


def s25_durable_update(env) -> bool:
    return stage_durable_record(env, 25)


CHECKS = [
    ("s25_authority_trace", s25_authority_trace, 2.0),
    ("s25_durable_update", s25_durable_update, 0.25),
]
