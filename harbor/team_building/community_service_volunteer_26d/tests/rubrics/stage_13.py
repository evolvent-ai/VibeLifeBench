from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s13_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 13)


def s13_durable_update(env) -> bool:
    return stage_durable_record(env, 13)


CHECKS = [
    ("s13_authority_trace", s13_authority_trace, 2.0),
    ("s13_durable_update", s13_durable_update, 0.25),
]
