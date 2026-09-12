from ._helpers import *

def s11_payment_failure_not_marked_paid(env) -> bool:
    return h_s11_payment_failure_not_marked_paid(env)

CHECKS = [
    ("s11_payment_failure_not_marked_paid", s11_payment_failure_not_marked_paid, 1.5),
]
