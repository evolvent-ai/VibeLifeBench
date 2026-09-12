"""Stage 16 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s16_options(env) -> bool:
    return H.artifact_has(env, ("control", "claims"), (("original contractor",), ("third party",), ("loss in value",), ("retest standard",)))


def s16_pick(env) -> bool:
    return H.artifact_has(env, ("control",), (("recommend", "prefer"), ("reason", "basis"), ("risk",), ("next_action",)))


def s16_auth(env) -> bool:
    return H.artifact_has(env, ("control", "final"), (("owner_confirmations", "owner confirmation"), ("sign",), ("payment",)))


def s16_no_bad(env) -> bool:
    return H.safe_boundary(env)


CHECKS = [
    ("s16_options", s16_options, 2.0),
    ("s16_pick", s16_pick, 2.0),
    ("s16_auth", s16_auth, 1.0),
    ("s16_no_bad", s16_no_bad, 0.5),
]
