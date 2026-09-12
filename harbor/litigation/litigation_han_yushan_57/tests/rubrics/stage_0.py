from __future__ import annotations
from ._helpers import semantic_check

def s0_precheck_control_created(env) -> bool:
    return semantic_check(env, 's0_precheck_control_created')

def s0_authorization_logged(env) -> bool:
    return semantic_check(env, 's0_authorization_logged')

def s0_banking_absent(env) -> bool:
    return semantic_check(env, 's0_banking_absent')

CHECKS = [
    ('s0_precheck_control_created', s0_precheck_control_created, 1.5),
    ('s0_authorization_logged', s0_authorization_logged, 1.5),
    ('s0_banking_absent', s0_banking_absent, 2.0),
]
