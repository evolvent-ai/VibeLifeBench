from __future__ import annotations
from ._helpers import *

def s1_listing_hard_filter(env) -> bool:
    return stage1_hard_filter_matrix(env) and tool_stage_results_cover(env, 1, LP, "search_listings", [C.LIST_C, C.LIST_F, C.LIST_G])

def s1_reject_no_elevator_high_floor(env) -> bool:
    return stage1_reject_f_no_elevator(env)

CHECKS = [
    ('s1_listing_hard_filter', s1_listing_hard_filter, 1.5),
    ('s1_reject_no_elevator_high_floor', s1_reject_no_elevator_high_floor, 2.0),
]
