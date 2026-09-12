from __future__ import annotations

from . import _helpers as h

def ck_13(env) -> bool:
    return h.check_ck_13(env)

def ck_14(env) -> bool:
    return h.check_ck_14(env)

def ck_15(env) -> bool:
    return h.check_ck_15(env)

CHECKS = [
    ("ck_13", ck_13, 2.0),
    ("ck_14", ck_14, 2.0),
    ("ck_15", ck_15, 1.5),
]
