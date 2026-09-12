"""Rubric predicate documentation."""
from __future__ import annotations

from .checks import s18_servers, s18_result

CHECKS = [
    ("s18_servers", s18_servers, 0.5),
    ("s18_result", s18_result, 2.0),
]
