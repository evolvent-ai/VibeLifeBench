from __future__ import annotations
from ._helpers import *

def s18_deadline_route_recovered(env) -> bool:
    return bool(
        notification_tool(env, 18, ('Qinghe Alternative Residence', 'route_refresh'))
        and tool_stage_object(env, 18, 'maps', None, C.PLACE_C, ('Qinghe Alternative Residence',))
        and tool_stage(env, 18, 'email', None, ('7118',))
        and email_message_has(env, C.EMAIL_DEADLINE, ('2026-08-07 18:00', '8580', 'quote expiration'))
        and place_has_parts(env, C.PLACE_C, ('east_gate_detour_2026_08_05',))
    )

def s18_shortlist_reordered(env) -> bool:
    return bool(
        email_message_has(env, C.EMAIL_DEADLINE, ('2026-08-07 18:00', 'repair', 'deposit'))
        and listing_status(env, C.LIST_C) == 'active'
        and listing_status(env, C.LIST_E) == 'active'
        and derived_stage_has(env, 18, (C.LIST_A, 'response deadline', C.LIST_C, 'alternative'), ('CANDIDATE_TRACKER.md', 'FINAL_REVIEW.md', 'RISK_LOG.md'))
    )

CHECKS = [
    ("s18_deadline_route_recovered", s18_deadline_route_recovered, 1.75),
    ("s18_shortlist_reordered", s18_shortlist_reordered, 1.5),
]
