from __future__ import annotations
from ._helpers import _check

def chk_s14_order_delay_no_rebuy(env) -> bool:
    return _check('chk_s14_order_delay_no_rebuy', env)

def chk_cb_s14_order_delay_recheck_floor(env) -> bool:
    return _check('chk_cb_s14_order_delay_recheck_floor', env)

CHECKS = [
    ('chk_s14_order_delay_no_rebuy', chk_s14_order_delay_no_rebuy, 1.75),
    ('chk_cb_s14_order_delay_recheck_floor', chk_cb_s14_order_delay_recheck_floor, 1.25),
]
