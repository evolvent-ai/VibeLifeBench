from __future__ import annotations
from ._helpers import check_s10_bank_authorization_guard

def s10_bank_authorization_guard(env) -> bool:
    return check_s10_bank_authorization_guard(env)

CHECKS = [
    ("s10_bank_authorization_guard", s10_bank_authorization_guard, 3),
]
