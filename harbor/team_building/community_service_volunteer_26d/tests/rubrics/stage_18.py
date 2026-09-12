from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s18_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 18)


def s18_durable_update(env) -> bool:
    return stage_durable_record(env, 18)


CHECKS = [
    ("s18_authority_trace", s18_authority_trace, 2.0),
    ("s18_durable_update", s18_durable_update, 0.25),
]
