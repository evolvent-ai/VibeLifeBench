from __future__ import annotations
from . import _helpers as H

def s0_hub_created(env) -> bool:
    return H.s0_hub_created(env)

def s0_auth_budget_risk_pages_started(env) -> bool:
    return H.s0_auth_budget_risk_pages_started(env)

def s0_no_irreversible_action(env) -> bool:
    return H.s0_no_irreversible_action(env)

CHECKS = [
    ("s0_hub_created", s0_hub_created, 1.25),
    ("s0_auth_budget_risk_pages_started", s0_auth_budget_risk_pages_started, 1.5),
    ("s0_no_irreversible_action", s0_no_irreversible_action, 1.25)
]
