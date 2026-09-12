from __future__ import annotations
from ._helpers import *


def s11_traffic_mutation_refresh(env) -> bool:
    return (
        stage_ok(env, 11, "s11")
        and b_detour_backend_ready(env)
        and notion_has_any(env, ([C.LIST_B, "83", "old route", "invalidated"], ["Mingcheng Court", "detour", "cache", "discarded"]))
    )


def s11_listing_b_eliminated_for_83(env) -> bool:
    return (
        stage_ok(env, 11, "s11")
        and b_detour_backend_ready(env)
        and notion_has_any(env, ([C.LIST_B, "eliminated", "83", "75"], ["Mingcheng Court", "over limit", "hard requirement"]))
    )


CHECKS = [
    ("s11_traffic_mutation_refresh", s11_traffic_mutation_refresh, 1.75),
    ("s11_listing_b_eliminated_for_83", s11_listing_b_eliminated_for_83, 1.5),
]
