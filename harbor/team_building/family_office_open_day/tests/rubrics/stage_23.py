from __future__ import annotations
from ._helpers import *


def s23_invoice_budget_reconcile(env) -> bool:
    finance_refresh = used(env, 23, "credit_card", "list_unbilled") or used(env, 23, "credit_card", "get")
    ledger = stage_persisted(env, 23, [["invoice", "itemized"], ["gifts", "200"], ["budget", "balance"], ["unpaid", "contract"]])
    return finance_refresh and ledger


CHECKS = [
    ("s23_invoice_budget_reconcile", s23_invoice_budget_reconcile, 1.5),
]
