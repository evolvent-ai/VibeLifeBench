from __future__ import annotations

from . import _helpers as h

def ck_04(env) -> bool:
    return h.check_ck_04(env)

def ck_05(env) -> bool:
    return h.check_ck_05(env)

CHECKS = [
    ("ck_04", ck_04, 2.0),
    ("ck_05", ck_05, 2.0),
]
