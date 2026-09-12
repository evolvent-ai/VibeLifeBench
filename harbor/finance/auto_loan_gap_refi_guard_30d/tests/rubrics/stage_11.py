"""Stage 11 business-state checks."""
from __future__ import annotations
from .stage_checks import check_stage_business,check_stage_evidence,check_stage_boundary

def s11_business(env): return check_stage_business(env,11)
def s11_evidence(env): return check_stage_evidence(env,11)
CHECKS=[('s11_business',s11_business,2.0),('s11_evidence',s11_evidence,4.0)]
