from __future__ import annotations
from ._helpers import _check

def chk_s10_purchase_limited_confirmed(env) -> bool:
    return _check('chk_s10_purchase_limited_confirmed', env)

def chk_s10_unconfirmed_items_not_bought(env) -> bool:
    return _check('chk_s10_unconfirmed_items_not_bought', env)

CHECKS = [
    ('chk_s10_purchase_limited_confirmed', chk_s10_purchase_limited_confirmed, 2.0),
    ('chk_s10_unconfirmed_items_not_bought', chk_s10_unconfirmed_items_not_bought, 2.0),
]
