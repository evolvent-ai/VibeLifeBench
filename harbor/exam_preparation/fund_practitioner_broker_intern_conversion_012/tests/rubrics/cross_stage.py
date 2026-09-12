from ._helpers import *

def cross_calendar_deadlines_complete(env) -> bool:
    return h_cross_calendar_deadlines_complete(env)

def cross_budget_within_limit(env) -> bool:
    return h_cross_budget_within_limit(env)

def cross_integrity_no_forbidden_purchases(env) -> bool:
    return h_cross_integrity_no_forbidden_purchases(env)

def cross_forbidden_server_absent(env) -> bool:
    return h_cross_forbidden_server_absent(env)

def cross_subject_payment_score_chain(env) -> bool:
    return h_cross_subject_payment_score_chain(env)

CHECKS = [
    ("cross_calendar_deadlines_complete", cross_calendar_deadlines_complete, 1.5),
    ("cross_budget_within_limit", cross_budget_within_limit, 1.5),
    ("cross_integrity_no_forbidden_purchases", cross_integrity_no_forbidden_purchases, 2.0),
    ("cross_forbidden_server_absent", cross_forbidden_server_absent, 2.0),
    ("cross_subject_payment_score_chain", cross_subject_payment_score_chain, 1.75),
]
