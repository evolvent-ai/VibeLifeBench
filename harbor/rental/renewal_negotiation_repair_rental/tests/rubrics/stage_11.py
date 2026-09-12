from __future__ import annotations
from ._helpers import *

def s11_low_price_not_promoted(env) -> bool:
    return bool(
        tool_stage_object(env, 11, 'review_platform', None, C.MER_B, ('Yongtaizhuang North Road',))
        and listing_attr(env, C.LIST_B, 'landlord_identity') == 'unverified'
        and review_has(env, C.MER_B, ('payment QR code', 'property owner'))
        and derived_stage_has(env, 11, (C.LIST_B, 'high risk'), ('CANDIDATE_TRACKER.md', 'RISK_LOG.md'))
    )

def s11_identity_review_checked(env) -> bool:
    return bool(
        tool_stage_object(env, 11, 'listing_platform', None, C.LIST_B, ('Yongtaizhuang North Road',))
        and tool_stage_object(env, 11, 'review_platform', None, C.MER_B, ('Yongtaizhuang North Road',))
        and listing_has_parts(env, C.LIST_B, ('personal_qr_code', 'contracting party', 'refund conditions'))
        and review_has(env, C.MER_B, ('payment QR code', 'property owner'))
    )

CHECKS = [
    ("s11_low_price_not_promoted", s11_low_price_not_promoted, 1.5),
    ("s11_identity_review_checked", s11_identity_review_checked, 1.25),
]
