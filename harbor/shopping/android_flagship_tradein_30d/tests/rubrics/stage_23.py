"""Stage 23 checks — Each check is an independent named function from checks.py."""
from __future__ import annotations

from .checks import s23_structured, s23_threads

CHECKS = [
    ("s23_structured", s23_structured, 2.0),
    ("s23_threads", s23_threads, 1.0),
]
