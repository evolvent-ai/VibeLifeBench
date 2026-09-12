"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s14_latest_finance_update_checked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s14_latest_finance_update_checked", env)

def s14_learning_budget_boundary_active(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s14_learning_budget_boundary_active", env)


CHECKS = [
    ("s14_latest_finance_update_checked", s14_latest_finance_update_checked, 0.5),
    ("s14_learning_budget_boundary_active", s14_learning_budget_boundary_active, 2.5),
]
