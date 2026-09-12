"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s12_venue_capacity_rechecked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s12_venue_capacity_rechecked", env)

def s12_cloud_loft_rejected(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s12_cloud_loft_rejected", env)


CHECKS = [
    ("s12_venue_capacity_rechecked", s12_venue_capacity_rechecked, 0.5),
    ("s12_cloud_loft_rejected", s12_cloud_loft_rejected, 0.5),
]
