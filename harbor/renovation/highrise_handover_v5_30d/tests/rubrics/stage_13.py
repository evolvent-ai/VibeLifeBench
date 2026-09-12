"""Stage 13 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s13_budget(env) -> bool:
    return H.artifact_has(env, ("claims",), (("charged",), ("disputed",), ("approved_not_received",), ("received",), ("reversed",), ("amount_minor",)))


CHECKS = [
    ("s13_budget", s13_budget, 3.0),
]
