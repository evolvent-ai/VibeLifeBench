"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s15_book_restock_rechecked(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s15_book_restock_rechecked", env)

def s15_cart_not_ordered(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s15_cart_not_ordered", env)


CHECKS = [
    ("s15_book_restock_rechecked", s15_book_restock_rechecked, 0.5),
    ("s15_cart_not_ordered", s15_cart_not_ordered, 0.75),
]
