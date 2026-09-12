"""Stage 5 checks — Each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s5_evidence

CHECKS = [
    ("s5_evidence", s5_evidence, 4.0),
]
