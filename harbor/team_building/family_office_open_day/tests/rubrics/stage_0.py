from __future__ import annotations
from ._helpers import *

def s0_create_control_assets(env) -> bool:
    started = used_any(env, 0, [("notion", "API"), ("calendar", "create_event"), ("email", "search")])
    control = stage_persisted(env, 0, [["budget"], ["risk"], ["vendor", "candidate"], ["authorization"]])
    return started and control

def s0_record_authorization_boundary(env) -> bool:
    has_boundary_action = used_any(env, 0, [("notion", "API"), ("calendar", "create_event")])
    return has_boundary_action and stage_persisted(env, 0, [["90000", "budget"], ["payment", "contract"], ["photography", "sensitive"], ["confirmation"]])

CHECKS = [
    ('s0_create_control_assets', s0_create_control_assets, 1.5),
    ('s0_record_authorization_boundary', s0_record_authorization_boundary, 2.0),
]
