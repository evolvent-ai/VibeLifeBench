"""Rubric contract documentation."""
from __future__ import annotations

from .checks import s19_result

CHECKS = [
    ("s19_result", s19_result, 2.5),
]
