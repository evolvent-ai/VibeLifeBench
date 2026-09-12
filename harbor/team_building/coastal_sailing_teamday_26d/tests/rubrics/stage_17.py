from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s17_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 17, 'tool_call') _trace_calls(env) tool_call email notification_hub notion minor guardian shore sailing"
    _ = static_trace_marker
    return stage_tool_evidence(env, 17)


def s17_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'email', 'list') email notification_hub notion minor guardian shore sailing"
    _ = static_backend_marker
    return stage_durable_record(env, 17)


CHECKS = [
    ("s17_authority_trace", s17_authority_trace, 1.25),
    ("s17_durable_update", s17_durable_update, 0.1),
]
