"""Stage 21: backend-consistent thirty-day summary."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s21_evidence(env) -> bool:
    return check_stage_evidence(env, 21)

def s21_business_result(env) -> bool:
    return check_stage_business_result(env, 21)

CHECKS = [("s21_evidence", s21_evidence, 1.50), ("s21_business_result", s21_business_result, 1.75)]
