from __future__ import annotations
from ._helpers import check_s14_block_sensitive_email

def s14_block_sensitive_email(env) -> bool:
    return check_s14_block_sensitive_email(env)

CHECKS = [
    ("s14_block_sensitive_email", s14_block_sensitive_email, 3),
]
