from __future__ import annotations
from ._helpers import check_s19_reconcile_ledger

def s19_reconcile_ledger(env) -> bool:
    return check_s19_reconcile_ledger(env)

CHECKS = [
    ("s19_reconcile_ledger", s19_reconcile_ledger, 2),
]
