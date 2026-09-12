from __future__ import annotations
from ._helpers import check_s9_quiet_gap

def s9_quiet_gap(env) -> bool:
    return check_s9_quiet_gap(env)

CHECKS = [
    ("s9_quiet_gap", s9_quiet_gap, 1),
]
