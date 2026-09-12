from __future__ import annotations
from . import _helpers as H

def s4_auth_remains_pending(env) -> bool:
    return H.s4_auth_remains_pending(env)

def s4_travel_constraint_recorded(env) -> bool:
    return H.s4_travel_constraint_recorded(env)

CHECKS = [
    ("s4_auth_remains_pending", s4_auth_remains_pending, 1.25),
    ("s4_travel_constraint_recorded", s4_travel_constraint_recorded, 1.0)
]
