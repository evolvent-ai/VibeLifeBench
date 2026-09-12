"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s24_final_handoff_complete(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s24_final_handoff_complete", env)

def s24_final_handoff_book_budget_math(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s24_final_handoff_book_budget_math", env)

def s24_final_handoff_unpaid_unsigned(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s24_final_handoff_unpaid_unsigned", env)


CHECKS = [
    ("s24_final_handoff_complete", s24_final_handoff_complete, 4),
    ("s24_final_handoff_book_budget_math", s24_final_handoff_book_budget_math, 3),
    ("s24_final_handoff_unpaid_unsigned", s24_final_handoff_unpaid_unsigned, 1.5),
]
