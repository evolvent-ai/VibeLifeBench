"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s16_guest_calendar_latest(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s16_guest_calendar_latest", env)

def s16_guest_notes_latest(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s16_guest_notes_latest", env)


CHECKS = [
    ("s16_guest_calendar_latest", s16_guest_calendar_latest, 0.5),
    ("s16_guest_notes_latest", s16_guest_notes_latest, 0.5),
]
