from __future__ import annotations

from . import _helpers as h

def ck_20(env) -> bool:
    return h.check_ck_20(env)

CHECKS = [
    ("ck_20", ck_20, 1.75),
]
