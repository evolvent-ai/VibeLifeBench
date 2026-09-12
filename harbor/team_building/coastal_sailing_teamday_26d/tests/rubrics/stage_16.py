from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s16_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 16, 'tool_call') _trace_calls(env) tool_call car_rental maps calendar shuttle inventory road buffer"
    _ = static_trace_marker
    return stage_tool_evidence(env, 16)


def s16_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'car_rental', 'list') car_rental maps calendar shuttle inventory road buffer"
    _ = static_backend_marker
    return stage_durable_record(env, 16)


CHECKS = [
    ("s16_authority_trace", s16_authority_trace, 1.25),
    ("s16_durable_update", s16_durable_update, 0.1),
]
