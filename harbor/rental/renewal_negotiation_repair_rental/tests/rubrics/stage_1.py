from __future__ import annotations
from ._helpers import *

def s1_search_and_save_dual_candidates(env) -> bool:
    return bool(
        tool_stage(env, 1, 'listing_platform', 'search', ('850000',))
        and tool_stage(env, 1, 'listing_platform', 'save', (C.LIST_A,))
        and tool_stage(env, 1, 'listing_platform', 'save', (C.LIST_C,))
        and saved_has(env, C.LIST_A)
        and saved_has(env, C.LIST_C)
        and listing_status(env, C.LIST_A) == 'active'
        and listing_status(env, C.LIST_C) == 'active'
    )

def s1_subscribe_renewal_watch(env) -> bool:
    return bool(
        tool_stage_group(env, 1, 'notification_hub', None, [('Qinghe Jiayuan',), ('Qinghe Alternative Residence',), ('price', 'status')])
        and subscription_has_parts(env, ('listing_platform', 'active', '850000'))
        and (
            subscription_has_parts(env, ('Qinghe Jiayuan',))
            or subscription_has_parts(env, ('Qinghe Alternative Residence',))
        )
        and derived_stage_has_any(env, 1, [('subscription', 'review'), ('price', 'status')], ('CANDIDATE_TRACKER.md', 'HEARTBEAT.md'))
    )

CHECKS = [
    ("s1_search_and_save_dual_candidates", s1_search_and_save_dual_candidates, 1.5),
    ("s1_subscribe_renewal_watch", s1_subscribe_renewal_watch, 1.25),
]
