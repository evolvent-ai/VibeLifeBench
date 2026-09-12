"""Rubric check inventory."""
from __future__ import annotations

from .checks import s5_evidence

CHECKS = [
    ("s5_evidence", s5_evidence, 4.0),
]
