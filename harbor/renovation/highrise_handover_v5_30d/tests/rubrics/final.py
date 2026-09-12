"""Final-bucket checks."""
from __future__ import annotations

from .shared import _helpers as H


def f_budget(env) -> bool:
    return H.artifact_has(env, ("claims", "final"), (("3717000", "37170"), ("23600", "236"), ("received",), ("reversed",), ("funds_reconciliation",)))


def f_risk(env) -> bool:
    return H.artifact_has(env, ("defects", "final"), (("exterior window",), ("floor drain",), ("entrance door",), ("open_blockers",), ("written_reservations",)))


def f_evidence(env) -> bool:
    return H.artifact_has(env, ("evidence",), (("evidence_id",), ("captured_at",), ("source",), ("related_item",), ("status",)))


def f_summary(env) -> bool:
    return H.artifact_has(env, ("final",), (("ready_to_sign",), ("open_blockers",), ("written_reservations",), ("funds_reconciliation",), ("owner_confirmations",)))


def f_tracker(env) -> bool:
    return all(H.artifact_fields(env, key) for key in ("control", "defects", "claims"))


def f_no_bad(env) -> bool:
    return H.safe_boundary(env)


CHECKS = [
    ("f_budget", f_budget, 4.5),
    ("f_risk", f_risk, 4.5),
    ("f_evidence", f_evidence, 4.5),
    ("f_summary", f_summary, 4.0),
    ("f_tracker", f_tracker, 3.0),
    ("f_no_bad", f_no_bad, 4.0),
]
