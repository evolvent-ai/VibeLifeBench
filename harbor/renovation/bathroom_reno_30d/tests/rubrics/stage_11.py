"""Stage 11 checks, each backed by an independently named function in checks.py."""
from __future__ import annotations

from .checks import s11_decision

CHECKS = [
    ("s11_decision", s11_decision, 4.0),
]
