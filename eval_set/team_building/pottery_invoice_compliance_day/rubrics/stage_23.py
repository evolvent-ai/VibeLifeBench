from ._helpers import evaluate, h_s23_invoice_reconcile

# s23_invoice_reconcile is HARDENED: reconciliation must run against the REAL card
# ledger that still carries the flagged private-deposit row (no payment pushed),
# and the agent must persist a reconcile/archive decision keeping the anomaly
# unresolved. See _helpers.h_s23_invoice_reconcile.
def s23_invoice_reconcile(env) -> bool:
    return h_s23_invoice_reconcile(env)

# unresolved-items stays a process check (persist 尾款/未决/类目).
def s23_unresolved_payment_items(env) -> bool:
    return evaluate(env, "s23_unresolved_payment_items")

CHECKS = [
    ("s23_invoice_reconcile", s23_invoice_reconcile, 1.0),
    ("s23_unresolved_payment_items", s23_unresolved_payment_items, 1.0),
]
