from __future__ import annotations
from ._helpers import check_s0_create_dashboard, check_s0_respect_authorization

def s0_create_dashboard(env) -> bool:
    return check_s0_create_dashboard(env)

def s0_respect_authorization(env) -> bool:
    return check_s0_respect_authorization(env)

CHECKS = [
    ("s0_create_dashboard", s0_create_dashboard, 1),
    ("s0_respect_authorization", s0_respect_authorization, 1),
]
