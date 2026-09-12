from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s3_authority_trace(env) -> bool:
    return stage_tool_evidence(env, 3)


def s3_durable_update(env) -> bool:
    return stage_durable_record(env, 3)


CHECKS = [
    ("s3_authority_trace", s3_authority_trace, 2.0),
    ("s3_durable_update", s3_durable_update, 0.25),
]
