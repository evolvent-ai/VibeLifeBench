from ._helpers import evaluate

def s22_feedback_ingested(env) -> bool:
    return evaluate(env, "s22_feedback_ingested")

def s22_sop_risk_items(env) -> bool:
    return evaluate(env, "s22_sop_risk_items")

CHECKS = [
    ("s22_feedback_ingested", s22_feedback_ingested, 1.0),
    ("s22_sop_risk_items", s22_sop_risk_items, 1.0),
]
