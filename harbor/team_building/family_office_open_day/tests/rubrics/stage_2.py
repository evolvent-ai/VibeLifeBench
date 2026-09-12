from __future__ import annotations
from ._helpers import *

def s2_finance_invoice_ledger(env) -> bool:
    checked_rules = used(env, 2, "email", "search") or used(env, 2, "email", "get")
    recorded = stage_persisted(env, 2, [["invoice"], ["gifts", "catering"], ["budget"], ["authorization", "confirmation"]])
    return checked_rules and recorded

CHECKS = [
    ('s2_finance_invoice_ledger', s2_finance_invoice_ledger, 1.5),
]
