"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s13_budget_snapshot_rows(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s13_budget_snapshot_rows", env)

def s13_pending_approval_noted(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s13_pending_approval_noted", env)


CHECKS = [
    ("s13_budget_snapshot_rows", s13_budget_snapshot_rows, 0.5),
    ("s13_pending_approval_noted", s13_pending_approval_noted, 0.5),
]
