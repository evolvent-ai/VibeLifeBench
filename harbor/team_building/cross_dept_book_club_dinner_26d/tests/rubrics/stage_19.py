"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s19_dinner_policy_rechecked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s19_dinner_policy_rechecked", env)

def s19_bad_dinner_rejected(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s19_bad_dinner_rejected", env)


CHECKS = [
    ("s19_dinner_policy_rechecked", s19_dinner_policy_rechecked, 0.5),
    ("s19_bad_dinner_rejected", s19_bad_dinner_rejected, 0.5),
]
