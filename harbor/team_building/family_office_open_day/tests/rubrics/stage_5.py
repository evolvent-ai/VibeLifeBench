from __future__ import annotations
from ._helpers import *


def s5_catering_labels_before_confirm(env) -> bool:
    product_checked = used(env, 5, "ecommerce", "search") or used(env, 5, "ecommerce", "get_product")
    cart_or_record = stage_persisted(env, 5, [["nut-free", "meal"], ["wristbands", "badges"], ["200", "gifts"], ["unpaid", "cart", "list"]])
    return product_checked and cart_or_record


CHECKS = [
    ("s5_catering_labels_before_confirm", s5_catering_labels_before_confirm, 2.0),
]
