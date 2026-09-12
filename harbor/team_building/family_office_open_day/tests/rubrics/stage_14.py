from __future__ import annotations
from ._helpers import *

def s14_two_plan_no_payment(env) -> bool:
    finance_checked = used(env, 14, "credit_card", "list") or used(env, 14, "ecommerce", "get_cart")
    plan_recorded = stage_persisted(env, 14, [["plan", "two"], ["budget"], ["risk"], ["unpaid", "pending"]])
    return finance_checked and plan_recorded

CHECKS = [
    ('s14_two_plan_no_payment', s14_two_plan_no_payment, 1.5),
]
