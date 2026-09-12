from __future__ import annotations
from ._helpers import *

def s6_mutation_route_discovered(env) -> bool:
    return (
        tool_stage(env, 6, 'maps', None, ['evt_a_bus_early'])
        and tool_stage(env, 6, 'listing_platform', None, [C.LIST_A])
        and stage_reply_has_any(env, 6, [['commute'], ['route'], ['train'], ['transfer'], ['morning']])
    )

def s6_status_propagated(env) -> bool:
    return (
        tool_stage(env, 6, 'notion', None, [C.LIST_A])
        and notion_has_parts(env, [C.LIST_A])
    )

CHECKS = [
    ('s6_mutation_route_discovered', s6_mutation_route_discovered, 1.75),
    ('s6_status_propagated', s6_status_propagated, 1.5),
]
