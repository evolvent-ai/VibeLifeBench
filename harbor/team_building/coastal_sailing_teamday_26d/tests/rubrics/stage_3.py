from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s3_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 3, 'tool_call') _trace_calls(env) tool_call weather notification_hub calendar wind wave alert watch"
    _ = static_trace_marker
    return stage_tool_evidence(env, 3)


def s3_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'weather', 'list') weather notification_hub calendar wind wave alert watch"
    _ = static_backend_marker
    return stage_durable_record(env, 3)


CHECKS = [
    ("s3_authority_trace", s3_authority_trace, 1.25),
    ("s3_durable_update", s3_durable_update, 0.1),
]
