"""Stage 11 checks — Each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s11_decision

CHECKS = [
    ("s11_decision", s11_decision, 4.0),
]
