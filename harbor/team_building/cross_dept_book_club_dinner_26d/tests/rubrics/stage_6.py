"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s6_book_stock_rechecked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s6_book_stock_rechecked", env)

def s6_no_stale_book_plan(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s6_no_stale_book_plan", env)


CHECKS = [
    ("s6_book_stock_rechecked", s6_book_stock_rechecked, 0.5),
    ("s6_no_stale_book_plan", s6_no_stale_book_plan, 0.5),
]
