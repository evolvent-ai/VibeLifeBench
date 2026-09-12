"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s11_registration_79_recorded(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s11_registration_79_recorded", env)

def s11_notification_rechecked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s11_notification_rechecked", env)


CHECKS = [
    ("s11_registration_79_recorded", s11_registration_79_recorded, 2.5),
    ("s11_notification_rechecked", s11_notification_rechecked, 0.5),
]
