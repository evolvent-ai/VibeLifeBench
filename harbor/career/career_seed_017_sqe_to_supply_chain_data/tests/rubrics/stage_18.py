from __future__ import annotations

from . import _helpers as h

def ck_32(env) -> bool:
    return h.check_ck_32(env)

def ck_33(env) -> bool:
    return h.check_ck_33(env)

CHECKS = [
    ("ck_32", ck_32, 1.0),
    ("ck_33", ck_33, 1.0),
]
