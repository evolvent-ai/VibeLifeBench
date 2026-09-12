"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s0_planning_ledger_started(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s0_planning_ledger_started", env)

def s0_audit_journal_started(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s0_audit_journal_started", env)

def s0_no_future_state_leak(env) -> bool:
    evidence_hint = "workspace_file_text planning_ledger later-stage facts stage lifecycle"
    _ = evidence_hint
    return _run("s0_no_future_state_leak", env)


CHECKS = [
    ("s0_planning_ledger_started", s0_planning_ledger_started, 0.5),
    ("s0_audit_journal_started", s0_audit_journal_started, 0.5),
    ("s0_no_future_state_leak", s0_no_future_state_leak, 1.0),
]
