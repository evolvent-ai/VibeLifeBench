from __future__ import annotations
from ._helpers import *

def s14_fresh_listing_status(env) -> bool:
    return (
        tool_stage(env, 14, 'listing_platform', None, [C.LIST_C])
        and listing_status(env, C.LIST_C) == 'active'
        and s14_final_candidate_refresh(env)
    )

def s14_final_candidate_refresh(env) -> bool:
    return (
        tool_stage(env, 14, 'maps', None, [C.PLACE_C])
        or tool_stage(env, 14, 'review_platform', None, [C.MER_C])
    )

CHECKS = [
    ('s14_fresh_listing_status', s14_fresh_listing_status, 1.25),
    ('s14_final_candidate_refresh', s14_final_candidate_refresh, 1.25),
]
