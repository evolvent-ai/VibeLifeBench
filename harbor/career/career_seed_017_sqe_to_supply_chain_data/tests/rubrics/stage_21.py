from __future__ import annotations

from . import _helpers as h

def ck_35(env) -> bool:
    return h.check_ck_35(env)

def ck_36(env) -> bool:
    return h.check_ck_36(env)

def ck_37(env) -> bool:
    return h.check_ck_37(env)

CHECKS = [
    ("ck_35", ck_35, 1.0),
    ("ck_36", ck_36, 1.75),
    ("ck_37", ck_37, 1.0),
]
