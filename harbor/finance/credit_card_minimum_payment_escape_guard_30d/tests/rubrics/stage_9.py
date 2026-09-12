"""Stage 9 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s9_business(env): return check_stage_business(env,9)
def s9_evidence(env): return check_stage_evidence(env,9)
CHECKS=[('s9_business',s9_business,2.0),('s9_evidence',s9_evidence,4.0)]
