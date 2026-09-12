"""Stage 22 checks, each backed by an independently named function in checks.py."""
from __future__ import annotations

from .checks import s22_consistency

CHECKS = [
    ("s22_consistency", s22_consistency, 2.0),
]
