from __future__ import annotations
from ._helpers import check_s2_detect_and_recover_delay

def s2_detect_and_recover_delay(env) -> bool:
    return check_s2_detect_and_recover_delay(env)

CHECKS = [
    ("s2_detect_and_recover_delay", s2_detect_and_recover_delay, 3),
]
