from __future__ import annotations
from ._helpers import check_s20_closure_cleanup

def s20_closure_cleanup(env) -> bool:
    return check_s20_closure_cleanup(env)

CHECKS = [
    ("s20_closure_cleanup", s20_closure_cleanup, 1),
]
