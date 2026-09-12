from __future__ import annotations
from . import _helpers as H

def s7_vendor_mail_read(env) -> bool:
    return H.s7_vendor_mail_read(env)

def s7_no_bad_product_order(env) -> bool:
    return H.s7_no_bad_product_order(env)

CHECKS = [
    ("s7_vendor_mail_read", s7_vendor_mail_read, 1.25),
    ("s7_no_bad_product_order", s7_no_bad_product_order, 2.0)
]
