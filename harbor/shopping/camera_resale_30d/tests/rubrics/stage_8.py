"""Stage 8 checks —  check  checks.py """
from __future__ import annotations

from .checks import s8_table, s8_optimal

CHECKS = [
    ("s8_table", s8_table, 4.0),
    ("s8_optimal", s8_optimal, 3.0),
]
