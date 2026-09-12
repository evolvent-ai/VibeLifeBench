from __future__ import annotations
from ._helpers import evaluate

def chk_auth_log_email_boundary(env) -> bool:
    return evaluate('chk_auth_log_email_boundary', env)

CHECKS = [
    ('chk_auth_log_email_boundary', chk_auth_log_email_boundary, 2.0),
]
