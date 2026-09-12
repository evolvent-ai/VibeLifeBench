"""Stage 20 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s20_servers(env) -> bool:
    return H.stage_servers(env, 20, ("credit_card", "notification_hub"), 1)


def s20_result(env) -> bool:
    return H.backend_has(env, "credit_card", "list_unbilled", (("tx_hhigh_pp",), ("-3717000",), ("handover claim", "handover compensation")), card_id="card_hhigh_01") and H.artifact_has(env, ("claims",), (("received",), ("3717000", "37170"), ("reversed",), ("warranty",)))


CHECKS = [
    ("s20_servers", s20_servers, 0.5),
    ("s20_result", s20_result, 2.5),
]
