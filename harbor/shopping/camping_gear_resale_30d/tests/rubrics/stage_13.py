"""Stage 13 checks; each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s13_budget

CHECKS = [
    ("s13_budget", s13_budget, 3.0),
]
