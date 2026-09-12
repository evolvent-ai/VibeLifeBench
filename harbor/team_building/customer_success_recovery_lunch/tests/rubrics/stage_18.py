from __future__ import annotations
from ._helpers import *

def s18_execution_readiness_card(env) -> bool:
    return any_write(env, 18) and state_has(env, 18, [['materials'], ['safety'], ['credentials'], ['halal', 'lactose-free', 'lactose', 'dairy'], ['contact']])

def s18_pre_event_refresh_matrix(env) -> bool:
    return stage_server_hits(env, 18, [('review_platform', None), ('maps', None), ('calendar', None), ('email', None)]) >= 2 and any_write(env, 18)

CHECKS = [
    ('s18_execution_readiness_card', s18_execution_readiness_card, 1.5),
    ('s18_pre_event_refresh_matrix', s18_pre_event_refresh_matrix, 1.0),
]
