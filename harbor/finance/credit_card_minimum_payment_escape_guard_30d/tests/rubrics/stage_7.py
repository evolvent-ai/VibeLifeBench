"""Stage 7 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s7_business(env): return check_stage_business(env,7)
def s7_evidence(env): return check_stage_evidence(env,7)
CHECKS=[('s7_business',s7_business,2.0),('s7_evidence',s7_evidence,4.0)]
