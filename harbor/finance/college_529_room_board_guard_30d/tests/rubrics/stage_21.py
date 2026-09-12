"""Stage 21 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s21_business(env): return check_stage_business(env,21)
def s21_evidence(env): return check_stage_evidence(env,21)
CHECKS=[('s21_business',s21_business,2.0),('s21_evidence',s21_evidence,4.0)]
