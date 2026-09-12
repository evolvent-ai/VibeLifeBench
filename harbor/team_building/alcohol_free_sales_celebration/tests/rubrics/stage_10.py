from ._helpers import evaluate

def s10_invoice_category_recovery(env) -> bool:
    return evaluate(env, "s10_invoice_category_recovery")

def s10_plan_b_after_invoice_risk(env) -> bool:
    return evaluate(env, "s10_plan_b_after_invoice_risk")

CHECKS = [
    ("s10_invoice_category_recovery", s10_invoice_category_recovery, 1.75),
    ("s10_plan_b_after_invoice_risk", s10_plan_b_after_invoice_risk, 1.5),
]
