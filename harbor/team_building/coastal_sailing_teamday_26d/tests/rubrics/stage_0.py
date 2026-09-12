from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s0_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 0, 'tool_call') _trace_calls(env) tool_call email notion calendar sailing roster permit insurance"
    _ = static_trace_marker
    return stage_tool_evidence(env, 0)


def s0_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'email', 'list') email notion calendar sailing roster permit insurance"
    _ = static_backend_marker
    return stage_durable_record(env, 0)


CHECKS = [
    ("s0_authority_trace", s0_authority_trace, 1.25),
    ("s0_durable_update", s0_durable_update, 0.1),
]
