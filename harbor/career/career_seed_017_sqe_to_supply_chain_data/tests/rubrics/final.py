from __future__ import annotations

from . import _helpers as h

def ck_38(env) -> bool:
    return h.check_ck_38(env)

def ck_39(env) -> bool:
    return h.check_ck_39(env)

def ck_40(env) -> bool:
    return h.check_ck_40(env)

CHECKS = [
    ("ck_38", ck_38, 1.75),
    ("ck_39", ck_39, 2.0),
    ("ck_40", ck_40, 1.25),
]
