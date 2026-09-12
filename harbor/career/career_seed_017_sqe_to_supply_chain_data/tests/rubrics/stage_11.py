from __future__ import annotations

from . import _helpers as h

def ck_21(env) -> bool:
    return h.check_ck_21(env)

CHECKS = [
    ("ck_21", ck_21, 2.0),
]
