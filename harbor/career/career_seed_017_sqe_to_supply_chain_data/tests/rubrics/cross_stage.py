from __future__ import annotations

from . import _helpers as h

def ck_03(env) -> bool:
    return h.check_ck_03(env)

def ck_29(env) -> bool:
    return h.check_ck_29(env)

def ck_34(env) -> bool:
    return h.check_ck_34(env)

CHECKS = [
    ("ck_03", ck_03, 1.5),
    ("ck_29", ck_29, 2.0),
    ("ck_34", ck_34, 1.25),
]
