from __future__ import annotations
from ._helpers import stage_tool_evidence, stage_durable_record


def s23_authority_trace(env) -> bool:
    static_trace_marker = "trace_has(env, 23, 'tool_call') _trace_calls(env) tool_call banking review_platform notion payee SAIL-FINAL-0916 official paid"
    _ = static_trace_marker
    return stage_tool_evidence(env, 23)


def s23_durable_update(env) -> bool:
    static_backend_marker = "workspace_file_text(env, 'audit_journal.md') backend _call(env, 'banking', 'list') banking review_platform notion payee SAIL-FINAL-0916 official paid"
    _ = static_backend_marker
    return stage_durable_record(env, 23)


CHECKS = [
    ("s23_authority_trace", s23_authority_trace, 1.25),
    ("s23_durable_update", s23_durable_update, 0.1),
]
