from __future__ import annotations

from . import _helpers as h

def ck_06(env) -> bool:
    return h.check_ck_06(env)

def ck_07(env) -> bool:
    return h.check_ck_07(env)

CHECKS = [
    ("ck_06", ck_06, 1.5),
    ("ck_07", ck_07, 1.25),
]
