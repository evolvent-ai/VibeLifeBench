from __future__ import annotations
from . import _helpers as H

def s11_gmat_fee_paid_once(env) -> bool:
    return H.s11_gmat_fee_paid_once(env)

def s11_payment_double_evidence(env) -> bool:
    return H.s11_payment_double_evidence(env)

CHECKS = [
    ("s11_gmat_fee_paid_once", s11_gmat_fee_paid_once, 2.0),
    ("s11_payment_double_evidence", s11_payment_double_evidence, 1.75)
]
