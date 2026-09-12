from ._helpers import *

def s13_portal_paid_verified_with_bank(env) -> bool:
    return h_s13_portal_paid_verified_with_bank(env)

def s13_budget_ledger_updated(env) -> bool:
    return h_s13_budget_ledger_updated(env)

CHECKS = [
    ("s13_portal_paid_verified_with_bank", s13_portal_paid_verified_with_bank, 1.75),
    ("s13_budget_ledger_updated", s13_budget_ledger_updated, 1.5),
]
