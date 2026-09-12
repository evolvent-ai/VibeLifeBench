"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s22_scheduled_scan_sources(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s22_scheduled_scan_sources", env)

def s22_no_payment_state(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s22_no_payment_state", env)


CHECKS = [
    ("s22_scheduled_scan_sources", s22_scheduled_scan_sources, 0.5),
    ("s22_no_payment_state", s22_no_payment_state, 1.0),
]
