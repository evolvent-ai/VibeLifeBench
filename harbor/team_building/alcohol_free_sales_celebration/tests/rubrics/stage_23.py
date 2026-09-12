from ._helpers import evaluate

def s23_invoice_reconcile(env) -> bool:
    return evaluate(env, "s23_invoice_reconcile")

def s23_unresolved_payment_items(env) -> bool:
    return evaluate(env, "s23_unresolved_payment_items")

CHECKS = [
    ("s23_invoice_reconcile", s23_invoice_reconcile, 1.75),
    ("s23_unresolved_payment_items", s23_unresolved_payment_items, 1.5),
]
