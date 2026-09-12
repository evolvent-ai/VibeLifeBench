from __future__ import annotations
from ._helpers import evaluate

def chk_s06_calendar_digest_checked(env) -> bool:
    return evaluate('chk_s06_calendar_digest_checked', env)

CHECKS = [
    ('chk_s06_calendar_digest_checked', chk_s06_calendar_digest_checked, 1.25),
]
