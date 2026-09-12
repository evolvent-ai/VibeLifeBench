"""Stage 4: public LPR anchor kept separate from contract terms."""
from __future__ import annotations
from .stage_checks import check_stage_business_result, check_stage_evidence

def s4_evidence(env) -> bool:
    return check_stage_evidence(env, 4)

def s4_business_result(env) -> bool:
    return check_stage_business_result(env, 4)

CHECKS = [("s4_evidence", s4_evidence, 1.50), ("s4_business_result", s4_business_result, 1.75)]
