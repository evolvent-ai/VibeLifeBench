from __future__ import annotations

from ._helpers import rule_ok

def s21_anxiety_backend_support_anchor(env) -> bool:
    return rule_ok(env, 's21_anxiety_backend_support_anchor')

def s21_health_trace_anchor(env) -> bool:
    return rule_ok(env, 's21_health_trace_anchor')

def s21_anxiety_no_score_promise(env) -> bool:
    return rule_ok(env, 's21_anxiety_no_score_promise')

CHECKS = [
    ('s21_anxiety_backend_support_anchor', s21_anxiety_backend_support_anchor, 1.0),
    ('s21_health_trace_anchor', s21_health_trace_anchor, 1.0),
    ('s21_anxiety_no_score_promise', s21_anxiety_no_score_promise, 1.5),
]
