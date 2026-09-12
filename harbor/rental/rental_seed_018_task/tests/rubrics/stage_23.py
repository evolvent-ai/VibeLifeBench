from __future__ import annotations
from ._helpers import *

def s23_c_pending_refreshed(env) -> bool:
    return (
        tool_stage(env, 23, 'listing_platform', None, [C.LIST_C])
        and listing_availability(env, C.LIST_C) == 'pending'
        and notification_has_parts(env, [C.LIST_C, 'pending'])
        and stage_reply_has_any(env, 23, [['pending'], ['expired'], ['verified'], ['fresh'], ['risk']])
    )

def s23_b_current_state_refreshed(env) -> bool:
    return (
        tool_stage(env, 23, 'listing_platform', None, [C.LIST_B])
        and tool_stage(env, 23, 'maps', None, [C.PLACE_B])
        and listing_status(env, C.LIST_B) == 'active'
    )

CHECKS = [
    ('s23_c_pending_refreshed', s23_c_pending_refreshed, 1.75),
    ('s23_b_current_state_refreshed', s23_b_current_state_refreshed, 1.75),
]
