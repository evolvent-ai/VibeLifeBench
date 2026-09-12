"""Stage 5 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s5_business(env): return check_stage_business(env,5)
def s5_evidence(env): return check_stage_evidence(env,5)
CHECKS=[('s5_business',s5_business,2.0),('s5_evidence',s5_evidence,4.0)]
