"""Stage 23 checks; each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s23_structured, s23_threads

CHECKS = [
    ("s23_structured", s23_structured, 2.0),
    ("s23_threads", s23_threads, 1.0),
]
