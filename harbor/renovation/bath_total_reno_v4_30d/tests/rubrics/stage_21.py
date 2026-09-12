"""Stage 21 checks — Each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s21_checklist

CHECKS = [
    ("s21_checklist", s21_checklist, 2.0),
]
