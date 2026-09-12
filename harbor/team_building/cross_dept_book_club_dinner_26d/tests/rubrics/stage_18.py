"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s18_dietary_update_recorded(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s18_dietary_update_recorded", env)

def s18_notifications_checked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s18_notifications_checked", env)


CHECKS = [
    ("s18_dietary_update_recorded", s18_dietary_update_recorded, 0.5),
    ("s18_notifications_checked", s18_notifications_checked, 3),
]
