from __future__ import annotations
from ._helpers import *


def s20_c_price_mutation_observed(env) -> bool:
    return stage20_c_price_refresh(env) and notion_has_any(env, ([C.LIST_C, "7350"], ["Hexi Qingyuan", "price cut", "7350"]))


def s20_c_route_still_eliminated(env) -> bool:
    return (
        stage20_c_route_still_blocked(env)
        and listing_c_route_over_limit(env)
        and notion_has_any(env, ([C.LIST_C, "route", "over limit", "eliminated"], ["Hexi Qingyuan", "price cut does not change", "75"]))
    )


CHECKS = [
    ("s20_c_price_mutation_observed", s20_c_price_mutation_observed, 1.25),
    ("s20_c_route_still_eliminated", s20_c_route_still_eliminated, 1.5),
]
