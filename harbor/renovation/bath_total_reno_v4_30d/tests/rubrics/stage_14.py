"""Stage 14 checks — Each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s14_servers, s14_result, s14_no_bad

CHECKS = [
    ("s14_servers", s14_servers, 0.5),
    ("s14_result", s14_result, 3.0),
    ("s14_no_bad", s14_no_bad, 0.5),
]
