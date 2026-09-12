"""Stage 18 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s18_servers(env) -> bool:
    return H.stage_servers(env, 18, ("credit_card", "notification_hub"), 1)


def s18_result(env) -> bool:
    return H.backend_has(env, "credit_card", "list_disputes", (("disp_hhigh_01",), ("approved",)), card_id="card_hhigh_01") and H.backend_has(env, "credit_card", "list_unbilled", (("tx_hhigh_rev",), ("-23600",)), card_id="card_hhigh_01") and H.artifact_has(env, ("claims",), (("approved", "approved"), ("reversed", "reversed"), ("23600", "236"), ("source",)))


CHECKS = [
    ("s18_servers", s18_servers, 0.5),
    ("s18_result", s18_result, 2.0),
]
