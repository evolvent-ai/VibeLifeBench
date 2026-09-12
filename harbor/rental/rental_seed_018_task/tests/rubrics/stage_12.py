from __future__ import annotations
from ._helpers import *

def s12_price_change_refresh(env) -> bool:
    return (
        tool_stage(env, 12, 'listing_platform', None, [C.LIST_A])
        and listing_price(env, C.LIST_A) == 920000
        and s12_budget_reclassification(env)
    )

def s12_budget_reclassification(env) -> bool:
    return (
        tool_stage(env, 12, 'notion', None, [C.LIST_A])
        and notion_has_parts(env, [C.LIST_A])
        and tool_stage(env, 12, 'calendar', None)
    )

CHECKS = [
    ('s12_price_change_refresh', s12_price_change_refresh, 1.75),
    ('s12_budget_reclassification', s12_budget_reclassification, 1.5),
]
