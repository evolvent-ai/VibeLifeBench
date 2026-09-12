from __future__ import annotations
from ._helpers import *

def s11_catering_label_hold(env) -> bool:
    return used(env, 11, 'review_platform', 'get_merchant_qa') and any_write(env, 11) and state_has(env, 11, [['lactose', 'milk'], ['halal', 'boxes'], ['label', 'hold']])

CHECKS = [
    ('s11_catering_label_hold', s11_catering_label_hold, 2.0),
]
