from __future__ import annotations
from ._helpers import *

def s6_mutation_rent_route_discovered(env) -> bool:
    return bool(
        tool_stage_object(env, 6, 'listing_platform', None, C.LIST_A, ('Qinghe Jiayuan',))
        and tool_stage_object(env, 6, 'maps', None, C.PLACE_A, ('Qinghe Jiayuan',))
        and listing_price(env, C.LIST_A) == 858000
        and listing_attr(env, C.LIST_A, 'night_access') == 'south_gate_after_22_30_reroute'
        and place_has_parts(env, C.PLACE_A, ('south_gate_after_22_30_reroute',))
    )

def s6_status_propagated_to_budget(env) -> bool:
    return bool(
        listing_price(env, C.LIST_A) == 858000
        and derived_stage_has(env, 6, (C.LIST_A, '858000', '850000', 'over budget'), ('BUDGET_LEDGER.md', 'CANDIDATE_TRACKER.md', 'RISK_LOG.md'))
    )

CHECKS = [
    ("s6_mutation_rent_route_discovered", s6_mutation_rent_route_discovered, 1.75),
    ("s6_status_propagated_to_budget", s6_status_propagated_to_budget, 1.5),
]
