from __future__ import annotations

from . import _helpers as h

def ck_22(env) -> bool:
    return h.check_ck_22(env)

CHECKS = [
    ("ck_22", ck_22, 1.0),
]
