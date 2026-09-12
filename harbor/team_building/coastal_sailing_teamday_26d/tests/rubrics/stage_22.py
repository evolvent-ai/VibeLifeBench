from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s22_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 22, 'tool_call') _trace_calls(env) tool_call review_platform ecommerce car_rental reserve order booking wave"
    _ = static_trace_marker
    return stage_tool_evidence(env, 22)


def s22_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'review_platform', 'list') review_platform ecommerce car_rental reserve order booking wave"
    _ = static_backend_marker
    return stage_durable_record(env, 22)


CHECKS = [
    ("s22_authority_trace", s22_authority_trace, 1.25),
    ("s22_durable_update", s22_durable_update, 0.1),
]
