from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s8_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 8, 'tool_call') _trace_calls(env) tool_call weather notification_hub calendar gale small craft hold no-go"
    _ = static_trace_marker
    return stage_tool_evidence(env, 8)


def s8_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'weather', 'list') weather notification_hub calendar gale small craft hold no-go"
    _ = static_backend_marker
    return stage_durable_record(env, 8)


CHECKS = [
    ("s8_authority_trace", s8_authority_trace, 1.25),
    ("s8_durable_update", s8_durable_update, 0.1),
]
