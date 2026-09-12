from __future__ import annotations
from . import _helpers as H

def s16_essay_policy_read(env) -> bool:
    return H.s16_essay_policy_read(env)

def s16_policy_light_refresh(env) -> bool:
    return H.s16_policy_light_refresh(env)

def s16_no_essay_product_order(env) -> bool:
    return H.s16_no_essay_product_order(env)

CHECKS = [
    ("s16_essay_policy_read", s16_essay_policy_read, 1.25),
    ("s16_policy_light_refresh", s16_policy_light_refresh, 1.0),
    ("s16_no_essay_product_order", s16_no_essay_product_order, 2.0)
]
