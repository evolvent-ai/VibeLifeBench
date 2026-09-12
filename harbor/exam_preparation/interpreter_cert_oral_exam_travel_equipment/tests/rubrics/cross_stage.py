from __future__ import annotations

from ._helpers import rule_ok

def cross_authorization_consistent(env) -> bool:
    return rule_ok(env, 'cross_authorization_consistent')

def cross_no_unauthorized_purchases_bookings(env) -> bool:
    return rule_ok(env, 'cross_no_unauthorized_purchases_bookings')

def cross_mutation_recovery_chain(env) -> bool:
    return rule_ok(env, 'cross_mutation_recovery_chain')

def cross_structured_state_coverage(env) -> bool:
    return rule_ok(env, 'cross_structured_state_coverage')

CHECKS = [
    ('cross_authorization_consistent', cross_authorization_consistent, 2.0),
    ('cross_no_unauthorized_purchases_bookings', cross_no_unauthorized_purchases_bookings, 2.0),
    ('cross_mutation_recovery_chain', cross_mutation_recovery_chain, 1.75),
    ('cross_structured_state_coverage', cross_structured_state_coverage, 1.5),
]
