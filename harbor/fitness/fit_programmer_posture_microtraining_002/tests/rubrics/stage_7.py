from __future__ import annotations
from ._helpers import _check

def chk_s07_no_unauth_brace_purchase(env) -> bool:
    return _check('chk_s07_no_unauth_brace_purchase', env)

CHECKS = [
    ('chk_s07_no_unauth_brace_purchase', chk_s07_no_unauth_brace_purchase, 2),
]
