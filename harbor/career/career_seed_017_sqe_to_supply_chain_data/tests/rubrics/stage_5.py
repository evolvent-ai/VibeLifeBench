from __future__ import annotations

from . import _helpers as h

def ck_12(env) -> bool:
    return h.check_ck_12(env)

CHECKS = [
    ("ck_12", ck_12, 1.25),
]
