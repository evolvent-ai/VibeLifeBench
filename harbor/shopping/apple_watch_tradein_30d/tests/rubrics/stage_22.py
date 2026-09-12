"""Rubric check inventory."""
from __future__ import annotations

from .checks import s22_consistency

CHECKS = [
    ("s22_consistency", s22_consistency, 2.0),
]
