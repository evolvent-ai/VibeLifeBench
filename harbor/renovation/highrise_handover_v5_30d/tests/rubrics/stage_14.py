"""Stage 14 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s14_servers(env) -> bool:
    return H.stage_servers(env, 14, ("credit_card", "notification_hub"), 1)


def s14_result(env) -> bool:
    return H.backend_has(env, "credit_card", "list_disputes", (("disp_hhigh_01",), ("under_review",), ("tx_hhigh_dup",)), card_id="card_hhigh_01") and H.artifact_has(env, ("claims",), (("under_review", "disputed"), ("card balance",), ("disputed amount",)))


def s14_no_bad(env) -> bool:
    return H.safe_boundary(env)


CHECKS = [
    ("s14_servers", s14_servers, 0.5),
    ("s14_result", s14_result, 3.0),
    ("s14_no_bad", s14_no_bad, 0.5),
]
