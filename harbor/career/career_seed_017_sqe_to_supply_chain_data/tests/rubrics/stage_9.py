from __future__ import annotations

from . import _helpers as h

def ck_18(env) -> bool:
    return h.check_ck_18(env)

def ck_19(env) -> bool:
    return h.check_ck_19(env)

CHECKS = [
    ("ck_18", ck_18, 1.5),
    ("ck_19", ck_19, 1.5),
]
