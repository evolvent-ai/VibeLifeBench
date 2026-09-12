from __future__ import annotations

from . import _helpers as h

def ck_30(env) -> bool:
    return h.check_ck_30(env)

def ck_31(env) -> bool:
    return h.check_ck_31(env)

CHECKS = [
    ("ck_30", ck_30, 1.0),
    ("ck_31", ck_31, 2.0),
]
