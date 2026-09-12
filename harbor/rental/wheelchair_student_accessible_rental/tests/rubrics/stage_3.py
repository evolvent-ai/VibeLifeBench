from __future__ import annotations
from ._helpers import *


def s3_commute_crosscheck_a_c(env) -> bool:
    return (
        stage_route_checked(env, 3, "a", max_minutes=35)
        and stage_route_checked(env, 3, "c", max_minutes=35)
        and stage_record_persisted(
            env,
            3,
            [("Luogui Jiayuan", C.LIST_A), ("Yunqi Court", C.LIST_C), ("Wuhan Donghu University laboratory building",), ("route", "commute")],
            files=("CANDIDATE_TRACKER.md",),
        )
    )


def s3_market_price_check(env) -> bool:
    market_read = tool_stage_predicate(
        env,
        3,
        "listing_platform",
        ("get_market_stats", "market_stats", "market"),
        lambda args: args.get("category") in (None, "rent")
        and _has_any_part(args, ("Wuhan", "Wuchang", "Hongshan", "Donghu")),
    )
    return (
        s3_commute_crosscheck_a_c(env)
        and market_read
        and candidate_c_backend_viable(env)
        and listing_price(env, C.LIST_C) <= C.PRICE_BUDGET_MINOR
    )


CHECKS = [
    ('s3_commute_crosscheck_a_c', s3_commute_crosscheck_a_c, 1.5),
    ('s3_market_price_check', s3_market_price_check, 1.25),
]
