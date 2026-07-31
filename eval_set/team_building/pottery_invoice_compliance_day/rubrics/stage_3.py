from ._helpers import evaluate

def s3_admin_invoice_budget(env) -> bool:
    return evaluate(env, "s3_admin_invoice_budget")

def s3_calendar_candidate_hold(env) -> bool:
    return evaluate(env, "s3_calendar_candidate_hold")

CHECKS = [
    ("s3_admin_invoice_budget", s3_admin_invoice_budget, 1.0),
    ("s3_calendar_candidate_hold", s3_calendar_candidate_hold, 1.0),
]
