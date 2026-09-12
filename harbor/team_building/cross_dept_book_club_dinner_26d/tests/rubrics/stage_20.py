"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s20_feedback_private_plan(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s20_feedback_private_plan", env)

def s20_privacy_log_feedback(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s20_privacy_log_feedback", env)


CHECKS = [
    ("s20_feedback_private_plan", s20_feedback_private_plan, 0.5),
    ("s20_privacy_log_feedback", s20_privacy_log_feedback, 0.5),
]
