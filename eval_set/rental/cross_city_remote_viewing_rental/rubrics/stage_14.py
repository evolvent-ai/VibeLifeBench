from __future__ import annotations
from ._helpers import *


def s14_fresh_listing_status(env) -> bool:
    return (
        listing_c_tool(env, 14)
        and listing_status(env, C.LIST_C) == "active"
        and listing_price(env, C.LIST_C) <= 600000
        and stage_any_structured_evidence(env, 14, [(C.LIST_C,), (C.LIST_C_NAME,), ("状态", "预算")])
    )


def s14_final_candidate_refresh(env) -> bool:
    return (
        s14_fresh_listing_status(env)
        and maps_c_tool(env, 14)
        and review_c_tool(env, 14)
    )


CHECKS = [
    ("s14_fresh_listing_status", s14_fresh_listing_status, 1.25),
    ("s14_final_candidate_refresh", s14_final_candidate_refresh, 1.25),
]
