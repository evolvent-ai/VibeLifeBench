from __future__ import annotations
from ._helpers import *


def s3_budget_nearby_refresh(env) -> bool:
    return (
        stage_ok(env, 3, "s3")
        and tool_stage_results_cover(env, 3, LP, "search_listings", [C.LIST_A, C.LIST_B, C.LIST_C, C.LIST_D, C.LIST_E])
        and all(listing_active_two_bed(env, x) for x in (C.LIST_A, C.LIST_B, C.LIST_C, C.LIST_D, C.LIST_E))
        and all(listing_price(env, x) <= 750000 for x in (C.LIST_A, C.LIST_B, C.LIST_D, C.LIST_E))
        and listing_price(env, C.LIST_C) in {735000, 760000}
        and notion_has_any(env, ([C.LIST_A, C.LIST_B, C.LIST_D, C.LIST_E, "7500"], ["Clear Bay Garden", "Mingcheng Court", "Yunanli", "South Creek Garden"]))
    )


def s3_keep_overbudget_history(env) -> bool:
    return (
        stage_ok(env, 3, "s3")
        and listing_active_two_bed(env, C.LIST_C)
        and listing_price(env, C.LIST_C) in {735000, 760000}
        and notion_has_any(env, ([C.LIST_C, "over budget", "retain history"], ["Hexi Qingyuan", "7600", "eliminated", "history"]))
    )


CHECKS = [
    ("s3_budget_nearby_refresh", s3_budget_nearby_refresh, 1.25),
    ("s3_keep_overbudget_history", s3_keep_overbudget_history, 1.25),
]
