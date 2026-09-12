from __future__ import annotations
from ._helpers import *

def cross_core_server_coverage(env) -> bool:
    return (
        used_servers_at_least(env, 7)
        and notification_tool(env, 23)
        and late_core_refresh(env)
        and closure_archive_refresh(env)
    )

def cross_candidate_b_remains_viable(env) -> bool:
    return (
        tool_stage(env, 23, 'listing_platform', None, [C.LIST_B])
        and tool_stage(env, 23, 'maps', None, [C.PLACE_B])
        and listing_status(env, C.LIST_B) == 'active'
        and listing_price(env, C.LIST_B) <= 900000
    )

def cross_authorization_boundary_consistent(env) -> bool:
    return (
        positive_authorization_work(env)
        and no_payment_or_contract_side_effect(env)
    )

CHECKS = [
    ('cross_core_server_coverage', cross_core_server_coverage, 1.5),
    ('cross_candidate_b_remains_viable', cross_candidate_b_remains_viable, 1.25),
    ('cross_authorization_boundary_consistent', cross_authorization_boundary_consistent, 2.0),
]
