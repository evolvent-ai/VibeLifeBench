from ._helpers import evaluate, h_s10_invoice_category_recovery

# s10_invoice_category_recovery is HARDENED to require the REAL post-mutation
# invoice flip (material-sales / needs-HQ) read from the review_platform backend,
# not a workspace keyword. See _helpers.h_s10_invoice_category_recovery.
def s10_invoice_category_recovery(env) -> bool:
    return h_s10_invoice_category_recovery(env)

# Plan-B remains a process check (persist a service-invoice alternative after the
# risk surfaces); left on evaluate() so a competent partial run still earns it.
def s10_plan_b_after_invoice_risk(env) -> bool:
    return evaluate(env, "s10_plan_b_after_invoice_risk")

CHECKS = [
    ("s10_invoice_category_recovery", s10_invoice_category_recovery, 1.0),
    ("s10_plan_b_after_invoice_risk", s10_plan_b_after_invoice_risk, 1.0),
]
