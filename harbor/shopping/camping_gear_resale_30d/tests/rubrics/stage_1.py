"""Stage 1 checks; each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s1_servers, s1_args, s1_result

CHECKS = [
    ("s1_servers", s1_servers, 0.5),
    ("s1_args", s1_args, 0.5),
    ("s1_result", s1_result, 1.0),
]
