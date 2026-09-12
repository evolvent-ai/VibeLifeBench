from __future__ import annotations
from ._helpers import check_s8_waitlist_recovery

def s8_waitlist_recovery(env) -> bool:
    return check_s8_waitlist_recovery(env)

CHECKS = [
    ("s8_waitlist_recovery", s8_waitlist_recovery, 3),
]
