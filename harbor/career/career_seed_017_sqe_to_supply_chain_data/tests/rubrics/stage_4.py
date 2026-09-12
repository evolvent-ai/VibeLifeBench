from __future__ import annotations

from . import _helpers as h

def ck_10(env) -> bool:
    return h.check_ck_10(env)

def ck_11(env) -> bool:
    return h.check_ck_11(env)

CHECKS = [
    ("ck_10", ck_10, 1.75),
    ("ck_11", ck_11, 1.5),
]
