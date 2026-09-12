from __future__ import annotations

from . import _helpers as h

def ck_16(env) -> bool:
    return h.check_ck_16(env)

def ck_17(env) -> bool:
    return h.check_ck_17(env)

CHECKS = [
    ("ck_16", ck_16, 1.5),
    ("ck_17", ck_17, 1.25),
]
