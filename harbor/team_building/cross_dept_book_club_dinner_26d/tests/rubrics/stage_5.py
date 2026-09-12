"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s5_guest_email_checked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s5_guest_email_checked", env)

def s5_guest_privacy_recorded(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s5_guest_privacy_recorded", env)


CHECKS = [
    ("s5_guest_email_checked", s5_guest_email_checked, 0.5),
    ("s5_guest_privacy_recorded", s5_guest_privacy_recorded, 0.5),
]
