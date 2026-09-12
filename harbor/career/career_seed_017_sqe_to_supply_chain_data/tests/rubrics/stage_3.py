from __future__ import annotations

from . import _helpers as h

def ck_08(env) -> bool:
    return h.check_ck_08(env)

def ck_09(env) -> bool:
    return h.check_ck_09(env)

CHECKS = [
    ("ck_08", ck_08, 1.25),
    ("ck_09", ck_09, 1.5),
]
