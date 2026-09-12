"""Stage 8 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s8_table(env) -> bool:
    return H.artifact_has(env, ("control", "claims"), (("rectification within a deadline",), ("third-party repair",), ("loss in value", "compensation"), ("completion period",), ("warranty",)))


def s8_optimal(env) -> bool:
    return H.artifact_has(env, ("control", "claims"), (("estimated",), ("approved_not_received", "approved but not received"), ("owner",), ("confirmation",)))


CHECKS = [
    ("s8_table", s8_table, 4.0),
    ("s8_optimal", s8_optimal, 3.0),
]
