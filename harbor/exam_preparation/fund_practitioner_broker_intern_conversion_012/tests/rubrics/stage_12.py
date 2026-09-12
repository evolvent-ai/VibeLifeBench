from ._helpers import *

def s12_payment_retry_authorized(env) -> bool:
    return h_s12_payment_retry_authorized(env)

CHECKS = [
    ("s12_payment_retry_authorized", s12_payment_retry_authorized, 2.0),
]
