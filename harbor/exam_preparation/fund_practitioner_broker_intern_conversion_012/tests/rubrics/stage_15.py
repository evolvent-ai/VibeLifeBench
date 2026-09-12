from ._helpers import *

def s15_errata_adjustment(env) -> bool:
    return h_s15_errata_adjustment(env)

def s15_qbank_purchase_authorized(env) -> bool:
    return h_s15_qbank_purchase_authorized(env)

CHECKS = [
    ("s15_errata_adjustment", s15_errata_adjustment, 1.75),
    ("s15_qbank_purchase_authorized", s15_qbank_purchase_authorized, 1.5),
]
