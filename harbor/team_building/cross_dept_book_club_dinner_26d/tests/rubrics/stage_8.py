"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s8_vendor_quotes_verified(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s8_vendor_quotes_verified", env)

def s8_venue_caveats_logged(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s8_venue_caveats_logged", env)


CHECKS = [
    ("s8_vendor_quotes_verified", s8_vendor_quotes_verified, 0.5),
    ("s8_venue_caveats_logged", s8_venue_caveats_logged, 0.5),
]
