"""Stage 6 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s6_servers(env) -> bool:
    return H.stage_servers(env, 6, ("credit_card", "email", "notification_hub"), 1)


def s6_args(env) -> bool:
    return H.stage_args(env, 6, ("card_hhigh_01", "BUILDING TEST LAB", "inspection"), 1)


def s6_result(env) -> bool:
    return H.backend_has(env, "notification_hub", "get_notification", (("ntf_hhigh_fx",), ("预授权", "preauthorization"), ("card_hhigh_01",)), notification_id="ntf_hhigh_fx") and H.artifact_has(env, ("claims",), (("estimated", "authorized"), ("currency", "currency"), ("preauthorization",)))


CHECKS = [
    ("s6_servers", s6_servers, 0.5),
    ("s6_args", s6_args, 0.5),
    ("s6_result", s6_result, 1.5),
]
