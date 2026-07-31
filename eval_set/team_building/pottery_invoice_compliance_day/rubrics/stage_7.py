from ._helpers import evaluate

def s7_approver_framework_draft(env) -> bool:
    return evaluate(env, "s7_approver_framework_draft")

def s7_budget_cap_visible(env) -> bool:
    return evaluate(env, "s7_budget_cap_visible")

CHECKS = [
    ("s7_approver_framework_draft", s7_approver_framework_draft, 1.0),
    ("s7_budget_cap_visible", s7_budget_cap_visible, 1.0),
]
