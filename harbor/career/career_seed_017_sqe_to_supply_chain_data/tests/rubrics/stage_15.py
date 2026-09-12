from __future__ import annotations

from . import _helpers as h

def ck_26(env) -> bool:
    return h.check_ck_26(env)

def ck_27(env) -> bool:
    return h.check_ck_27(env)

def ck_28(env) -> bool:
    return h.check_ck_28(env)

CHECKS = [
    ("ck_26", ck_26, 1.0),
    ("ck_27", ck_27, 2.0),
    ("ck_28", ck_28, 1.0),
]
