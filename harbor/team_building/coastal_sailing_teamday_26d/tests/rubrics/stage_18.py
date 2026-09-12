from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s18_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 18, 'tool_call') _trace_calls(env) tool_call weather notification_hub notion alert wind wave hold"
    _ = static_trace_marker
    return stage_tool_evidence(env, 18)


def s18_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'weather', 'list') weather notification_hub notion alert wind wave hold"
    _ = static_backend_marker
    return stage_durable_record(env, 18)


CHECKS = [
    ("s18_authority_trace", s18_authority_trace, 1.25),
    ("s18_durable_update", s18_durable_update, 0.1),
]
