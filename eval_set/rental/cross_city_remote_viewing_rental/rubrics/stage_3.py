from __future__ import annotations
from ._helpers import *


def s3_commute_crosscheck_a_c(env) -> bool:
    return (
        tool_stage(env, 3, "maps", None, (C.DESTINATION,))
        and tool_stage_any(env, 3, [
            ("maps", None, (C.PLACE_A,)),
            ("maps", None, (C.PLACE_C,)),
        ])
        and maps_route_available(env, C.PLACE_C, C.DESTINATION)
        and listing_within_budget(env, C.LIST_C)
        and stage_any_structured_evidence(env, 3, [(C.PLACE_C,), (C.LIST_C,), (C.LIST_C_NAME,)])
    )


def s3_market_price_check(env) -> bool:
    return (
        tool_stage(env, 3, "listing_platform", "market", ("rent",))
        and listing_within_budget(env, C.LIST_C)
        and stage_structured_evidence(env, 3, ("市场价", "6000"))
    )


CHECKS = [
    ("s3_commute_crosscheck_a_c", s3_commute_crosscheck_a_c, 1.5),
    ("s3_market_price_check", s3_market_price_check, 1.25),
]
