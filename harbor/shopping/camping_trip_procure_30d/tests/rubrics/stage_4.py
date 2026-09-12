"""Rubric predicate documentation."""
from __future__ import annotations

from .checks import s4_servers, s4_reject

CHECKS = [
    ("s4_servers", s4_servers, 0.5),
    ("s4_reject", s4_reject, 4.0),
]
