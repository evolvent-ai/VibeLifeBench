"""Stage 21 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s21_checklist(env) -> bool:
    return H.artifact_has(env, ("control", "defects", "final"), (("keys",), ("documents",), ("exterior windows",), ("floor drains",), ("entrance door",), ("owner_confirmations",)))


CHECKS = [
    ("s21_checklist", s21_checklist, 2.0),
]
