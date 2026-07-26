from __future__ import annotations
from ._helpers import *


def s8_price_change_refresh(env) -> bool:
    return (
        tool_stage(env, 8, "listing_platform", None, (C.LIST_B,))
        and tool_stage(env, 8, "listing_platform", None, (C.LIST_C,))
        and listing_price(env, C.LIST_B) == 630000
        and stage_any_structured_evidence(env, 8, [(C.LIST_B, "6300"), (C.LIST_B, "超预算"), ("预算", "6300")])
    )


def s8_budget_reclassification(env) -> bool:
    return (
        s8_price_change_refresh(env)
        and listing_over_budget(env, C.LIST_B)
        and stage_structured_evidence(env, 8, (C.LIST_B, "6300"))
    )


CHECKS = [
    ("s8_price_change_refresh", s8_price_change_refresh, 1.75),
    ("s8_budget_reclassification", s8_budget_reclassification, 1.5),
]
