from __future__ import annotations
from ._helpers import *


def s11_roommate_noise_review(env) -> bool:
    return (
        tool_stage(env, 11, "review_platform", None, (C.MER_B,))
        and tool_stage(env, 11, "listing_platform", None, (C.LIST_B,))
        and review_has(env, C.MER_B, ("物业",))
    )


def s11_low_price_not_promoted(env) -> bool:
    return (
        stage_b_listing_review_email_mapping(env, 11)
        and listing_b_has_private_payment_and_gate_risk(env)
        and stage_structured_evidence(env, 11, (C.LIST_B, "风险"))
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [
    ("s11_roommate_noise_review", s11_roommate_noise_review, 1.25),
    ("s11_low_price_not_promoted", s11_low_price_not_promoted, 1.5),
]
