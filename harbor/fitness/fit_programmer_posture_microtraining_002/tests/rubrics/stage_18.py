from __future__ import annotations
from ._helpers import _check

def chk_s18_order_delay_adjustment(env) -> bool:
    return _check('chk_s18_order_delay_adjustment', env)

def chk_s18_diff_order_delay_no_duplicate(env) -> bool:
    return _check('chk_s18_diff_order_delay_no_duplicate', env)

CHECKS = [
    ('chk_s18_order_delay_adjustment', chk_s18_order_delay_adjustment, 1.75),
    ('chk_s18_diff_order_delay_no_duplicate', chk_s18_diff_order_delay_no_duplicate, 1.5),
]
