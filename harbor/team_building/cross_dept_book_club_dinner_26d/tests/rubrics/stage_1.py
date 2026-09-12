"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s1_initial_sources_queried(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s1_initial_sources_queried", env)

def s1_procurement_tracker_created(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s1_procurement_tracker_created", env)


CHECKS = [
    ("s1_initial_sources_queried", s1_initial_sources_queried, 0.5),
    ("s1_procurement_tracker_created", s1_procurement_tracker_created, 0.5),
]
