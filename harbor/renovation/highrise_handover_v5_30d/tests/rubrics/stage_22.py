"""Stage 22 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s22_consistency(env) -> bool:
    return H.artifact_has(env, ("control", "defects", "claims", "evidence"), (("developer",), ("property management",), ("bank",), ("source",), ("updated_at",), ("conflict", "inconsistency")))


CHECKS = [
    ("s22_consistency", s22_consistency, 2.0),
]
