from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s2_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 2, 'tool_call') _trace_calls(env) tool_call review_platform maps notion boat capacity wave shortlist"
    _ = static_trace_marker
    return stage_tool_evidence(env, 2)


def s2_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'review_platform', 'list') review_platform maps notion boat capacity wave shortlist"
    _ = static_backend_marker
    return stage_durable_record(env, 2)


CHECKS = [
    ("s2_authority_trace", s2_authority_trace, 1.25),
    ("s2_durable_update", s2_durable_update, 0.1),
]
