from ._helpers import evaluate

def s14_user_confirmation_pack(env) -> bool:
    return evaluate(env, "s14_user_confirmation_pack")

def s14_approval_pack_budget_safety(env) -> bool:
    return evaluate(env, "s14_approval_pack_budget_safety")

CHECKS = [
    ("s14_user_confirmation_pack", s14_user_confirmation_pack, 1.0),
    ("s14_approval_pack_budget_safety", s14_approval_pack_budget_safety, 1.0),
]
