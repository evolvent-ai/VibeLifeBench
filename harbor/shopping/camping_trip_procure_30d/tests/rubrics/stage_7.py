"""Rubric predicate documentation."""
from __future__ import annotations

from .checks import s7_servers, s7_args, s7_result

CHECKS = [
    ("s7_servers", s7_servers, 0.5),
    ("s7_args", s7_args, 0.5),
    ("s7_result", s7_result, 1.0),
]
