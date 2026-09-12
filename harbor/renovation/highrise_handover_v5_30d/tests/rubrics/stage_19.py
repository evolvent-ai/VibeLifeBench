"""Stage 19 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s19_result(env) -> bool:
    return H.backend_has(env, "ecommerce", "get_order", (("ref_hhigh_b",), ("approved",), ("3540000",)), order_id="ord_hhigh_0001") and H.artifact_has(env, ("defects", "claims"), (("approved_not_received", "approved"), ("missing document page", "entrance door"), ("next_action",)))


CHECKS = [
    ("s19_result", s19_result, 2.5),
]
