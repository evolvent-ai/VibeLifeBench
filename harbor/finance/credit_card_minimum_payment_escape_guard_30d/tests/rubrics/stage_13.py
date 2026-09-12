"""Stage 13 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s13_business(env): return check_stage_business(env,13)
def s13_evidence(env): return check_stage_evidence(env,13)
CHECKS=[('s13_business',s13_business,2.0),('s13_evidence',s13_evidence,4.0)]
