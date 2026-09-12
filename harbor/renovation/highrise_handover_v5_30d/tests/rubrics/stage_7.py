"""Stage 7 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s7_servers(env) -> bool:
    return H.stage_servers(env, 7, ("notification_hub", "ecommerce"), 1)


def s7_args(env) -> bool:
    return H.stage_args(env, 7, ("ntf_hhigh_cp", "ord_hhigh_0001"), 1)


def s7_result(env) -> bool:
    return H.backend_has(env, "notification_hub", "get_notification", (("局部维修", "limited repair"), ("排除", "不包含", "exclusion", "not included"), ("关闭", "closure")), notification_id="ntf_hhigh_cp") and H.artifact_has(env, ("control", "claims"), (("coverage",), ("exclusion",), ("closure",)))


CHECKS = [
    ("s7_servers", s7_servers, 0.5),
    ("s7_args", s7_args, 0.5),
    ("s7_result", s7_result, 1.0),
]
