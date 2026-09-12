"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s21_correct_reversible_holds(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s21_correct_reversible_holds", env)

def s21_book_cart_ready_no_order(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s21_book_cart_ready_no_order", env)

def s21_book_budget_math_ready(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s21_book_budget_math_ready", env)


CHECKS = [
    ("s21_correct_reversible_holds", s21_correct_reversible_holds, 5),
    ("s21_book_cart_ready_no_order", s21_book_cart_ready_no_order, 5),
    ("s21_book_budget_math_ready", s21_book_budget_math_ready, 3),
]
