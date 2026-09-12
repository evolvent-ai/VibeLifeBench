from __future__ import annotations

from . import _helpers as h

def ck_23(env) -> bool:
    return h.check_ck_23(env)

def ck_24(env) -> bool:
    return h.check_ck_24(env)

def ck_25(env) -> bool:
    return h.check_ck_25(env)

CHECKS = [
    ("ck_23", ck_23, 2.0),
    ("ck_24", ck_24, 2.0),
    ("ck_25", ck_25, 2.0),
]
