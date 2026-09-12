from __future__ import annotations
from ._helpers import *

def s2_finance_invoice_ledger(env) -> bool:
    return used(env, 2, 'email') and state_has(env, 2, [['32000'], ['invoice'], ['alcohol'], ['budget']])

CHECKS = [
    ('s2_finance_invoice_ledger', s2_finance_invoice_ledger, 1.5),
]
