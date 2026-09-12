from __future__ import annotations
from ._helpers import *

def s0_create_control_assets(env) -> bool:
    return (used(env, 0, 'notion', 'API-post-page') and used(env, 0, 'calendar', 'create_event')) and state_has(env, 0, [['budget'], ['risk'], ['candidate', 'vendor'], ['authorization']])

def s0_record_authorization_boundary(env) -> bool:
    return (used(env, 0, 'notion', 'API-post-page') or used(env, 0, 'email', 'save_draft')) and state_has(env, 0, [['8000'], ['payment', 'plan'], ['sensitive'], ['confirmation']])

CHECKS = [
    ('s0_create_control_assets', s0_create_control_assets, 1.5),
    ('s0_record_authorization_boundary', s0_record_authorization_boundary, 2.0),
]
