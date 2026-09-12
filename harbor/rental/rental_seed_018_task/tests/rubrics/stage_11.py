from __future__ import annotations
from ._helpers import *

def s11_roommate_noise_review(env) -> bool:
    return (
        tool_stage(env, 11, 'review_platform', None, [C.MER_B])
        and tool_stage(env, 11, 'listing_platform', None, [C.LIST_B])
        and stage_reply_has_any(env, 11, [['risk'], ['management'], ['review'], ['documents'], ['private']])
    )

def s11_low_price_not_promoted(env) -> bool:
    return (
        s11_roommate_noise_review(env)
        and tool_stage(env, 11, 'notion', None, [C.LIST_B])
        and notion_has_parts(env, [C.LIST_B])
        and tool_stage(env, 11, 'email', None)
        and no_payment_or_contract_side_effect(env)
    )

CHECKS = [
    ('s11_roommate_noise_review', s11_roommate_noise_review, 1.25),
    ('s11_low_price_not_promoted', s11_low_price_not_promoted, 1.5),
]
