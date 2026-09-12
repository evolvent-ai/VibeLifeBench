"""Stage 23 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s23_structured(env) -> bool:
    return all(H.artifact_fields(env, key) for key in ("control", "defects", "claims", "evidence", "final"))


def s23_threads(env) -> bool:
    return H.artifact_has(env, ("final",), (("ready_to_sign",), ("open_blockers",), ("written_reservations",), ("funds_reconciliation",), ("owner_confirmations",)))


CHECKS = [
    ("s23_structured", s23_structured, 2.0),
    ("s23_threads", s23_threads, 1.0),
]
