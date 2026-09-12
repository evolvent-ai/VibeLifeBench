"""Stage 9 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s9_servers(env) -> bool:
    return H.stage_servers(env, 9, ("ecommerce", "notification_hub"), 1)


def s9_args(env) -> bool:
    return H.stage_args(env, 9, ("ref_hhigh_b", "exterior window"), 1)


def s9_result(env) -> bool:
    return H.backend_has(env, "ecommerce", "get_order", (("ref_hhigh_b",), ("rejected",), ("3540000",)), order_id="ord_hhigh_0001") and H.artifact_has(env, ("evidence",), (("unit number",), ("rainfall",), ("continuous video",), ("original",)))


CHECKS = [
    ("s9_servers", s9_servers, 0.5),
    ("s9_args", s9_args, 0.5),
    ("s9_result", s9_result, 2.5),
]
