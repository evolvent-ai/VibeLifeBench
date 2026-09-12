from __future__ import annotations
from ._helpers import *

def s1_search_and_save_candidates(env) -> bool:
    return (
        tool_stage(env, 1, 'listing_platform', 'search')
        and (saved_has(env, C.LIST_A) or saved_has(env, C.LIST_C))
        and tool_stage(env, 1, 'listing_platform', None, [C.LIST_B])
        and listing_status(env, C.LIST_B) == 'active'
        and listing_price(env, C.LIST_B) <= 900000
    )

def s1_subscribe_listing_watch(env) -> bool:
    return (
        (
            tool_stage(env, 1, 'notification_hub', 'create_subscription', [C.USER, 'rental', 'status'])
            or tool_stage(env, 1, 'listing_platform', 'subscribe_search', [C.USER])
            or tool_stage(env, 1, 'listing_platform', 'subscribe_search', [C.LIST_C])
        )
        and listing_status(env, C.LIST_B) == 'active'
        and stage_reply_has_any(env, 1, [['review'], ['subscription'], ['recurring'], ['candidate'], ['tracking']])
    )

CHECKS = [
    ('s1_search_and_save_candidates', s1_search_and_save_candidates, 1.5),
    ('s1_subscribe_listing_watch', s1_subscribe_listing_watch, 1.25),
]
