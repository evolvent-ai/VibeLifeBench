from __future__ import annotations

from . import _helpers as h

def ck_01(env) -> bool:
    return h.check_ck_01(env)

def ck_02(env) -> bool:
    return h.check_ck_02(env)

CHECKS = [
    ("ck_01", ck_01, 1.25),
    ("ck_02", ck_02, 2.0),
]
