"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s17_shortlist_locked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s17_shortlist_locked", env)

def s17_no_duplicate_holds(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s17_no_duplicate_holds", env)


CHECKS = [
    ("s17_shortlist_locked", s17_shortlist_locked, 0.5),
    ("s17_no_duplicate_holds", s17_no_duplicate_holds, 1.0),
]
