"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s25_feedback_archive_private(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s25_feedback_archive_private", env)

def s25_no_public_feedback_note(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s25_no_public_feedback_note", env)


CHECKS = [
    ("s25_feedback_archive_private", s25_feedback_archive_private, 4),
    ("s25_no_public_feedback_note", s25_no_public_feedback_note, 1.0),
]
