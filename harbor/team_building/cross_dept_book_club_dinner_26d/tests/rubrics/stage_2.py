"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s2_registration_snapshot_recorded(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s2_registration_snapshot_recorded", env)

def s2_notification_checked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s2_notification_checked", env)


CHECKS = [
    ("s2_registration_snapshot_recorded", s2_registration_snapshot_recorded, 0.5),
    ("s2_notification_checked", s2_notification_checked, 0.5),
]
