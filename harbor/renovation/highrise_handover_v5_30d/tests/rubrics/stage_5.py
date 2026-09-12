"""Stage 5 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s5_evidence(env) -> bool:
    return H.artifact_has(env, ("evidence",), (("documents",), ("inside the unit", "unit interior"), ("common areas",), ("communications",), ("funds",), ("captured_at",)))


CHECKS = [
    ("s5_evidence", s5_evidence, 4.0),
]
