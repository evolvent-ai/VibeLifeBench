"""Stage 3 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s3_servers(env) -> bool:
    return H.stage_servers(env, 3, ("ecommerce", "notification_hub"), 1)


def s3_args(env) -> bool:
    return H.stage_args(env, 3, ("ord_hhigh_0001", "ref_hhigh_b"), 1)


def s3_result(env) -> bool:
    return H.backend_has(env, "ecommerce", "get_order", (("ref_hhigh_b",), ("submitted",), ("3540000",)), order_id="ord_hhigh_0001") and H.artifact_has(env, ("defects",), (("submitted", "recorded"), ("exterior window",), ("floor drain",)))


CHECKS = [
    ("s3_servers", s3_servers, 0.5),
    ("s3_args", s3_args, 1.0),
    ("s3_result", s3_result, 2.0),
]
