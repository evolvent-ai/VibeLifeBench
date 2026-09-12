from __future__ import annotations
from ._helpers import *

def s8_price_change_refresh(env) -> bool:
    return bool(
        tool_stage_object(env, 8, 'listing_platform', None, C.LIST_B, ('Yongtaizhuang North Road',))
        and listing_price(env, C.LIST_B) == 730000
        and listing_attr(env, C.LIST_B, 'cleaning_fee_minor') == 180000
        and listing_attr(env, C.LIST_B, 'landlord_identity') == 'unverified'
    )

def s8_budget_reclassification(env) -> bool:
    return bool(
        listing_price(env, C.LIST_A) == 858000
        and listing_price(env, C.LIST_B) == 730000
        and listing_attr(env, C.LIST_B, 'cleaning_fee_minor') == 180000
        and derived_stage_has(env, 8, (C.LIST_A, '858000', 'over budget'), ('BUDGET_LEDGER.md', 'CANDIDATE_TRACKER.md'))
        and derived_stage_has(env, 8, (C.LIST_B, '730000', '180000', 'high risk'), ('BUDGET_LEDGER.md', 'RISK_LOG.md'))
    )

CHECKS = [
    ("s8_price_change_refresh", s8_price_change_refresh, 1.75),
    ("s8_budget_reclassification", s8_budget_reclassification, 1.5),
]
