"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s9_guest_update_read(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s9_guest_update_read", env)

def s9_calendar_guest_hold(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s9_calendar_guest_hold", env)


CHECKS = [
    ("s9_guest_update_read", s9_guest_update_read, 0.5),
    ("s9_calendar_guest_hold", s9_calendar_guest_hold, 0.5),
]
