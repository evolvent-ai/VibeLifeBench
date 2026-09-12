from __future__ import annotations
from ._helpers import *

def s14_fresh_listing_status(env) -> bool:
    return bool(
        tool_stage_object(env, 14, 'listing_platform', None, C.LIST_A, ('Qinghe Jiayuan',))
        and tool_stage_object(env, 14, 'listing_platform', None, C.LIST_C, ('Qinghe Alternative Residence',))
        and tool_stage_result_has(env, 14, 'listing_platform', None, (C.LIST_A, '858000', 'active'))
        and tool_stage_result_has(env, 14, 'listing_platform', None, (C.LIST_C, '695000', 'active'))
        and listing_status(env, C.LIST_A) == 'active'
        and listing_status(env, C.LIST_C) == 'active'
    )

def s14_final_candidate_refresh(env) -> bool:
    return bool(
        s14_fresh_listing_status(env)
        and derived_stage_has(env, 14, ('preferred choice', C.LIST_A, 'over budget', 'alternative', C.LIST_C), ('CANDIDATE_TRACKER.md', 'RISK_LOG.md', 'BUDGET_LEDGER.md'))
    )

CHECKS = [
    ("s14_fresh_listing_status", s14_fresh_listing_status, 1.25),
    ("s14_final_candidate_refresh", s14_final_candidate_refresh, 1.25),
]
