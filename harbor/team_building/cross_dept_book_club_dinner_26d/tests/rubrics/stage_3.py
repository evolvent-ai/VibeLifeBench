"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s3_group_roster_mixed_departments(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s3_group_roster_mixed_departments", env)

def s3_dietary_privacy_noted(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s3_dietary_privacy_noted", env)


CHECKS = [
    ("s3_group_roster_mixed_departments", s3_group_roster_mixed_departments, 0.5),
    ("s3_dietary_privacy_noted", s3_dietary_privacy_noted, 0.5),
]
