from __future__ import annotations
from ._helpers import *

def s8_listing_search_constraints(env) -> bool:
    return stage_listing_search_constraints(env, 8)

def s8_requirements_propagated(env) -> bool:
    return tool_stage(env, 8, 'notion', None, ['ground floor']) and tool_stage(env, 8, 'notion', None, ['partition'])

CHECKS = [
    ('s8_listing_search_constraints', s8_listing_search_constraints, 1.5),
    ('s8_requirements_propagated', s8_requirements_propagated, 1.25),
]
