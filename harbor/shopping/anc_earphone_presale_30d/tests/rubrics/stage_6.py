"""Stage 6 checks — each check is an independently named function in checks.py。"""
from __future__ import annotations

from .checks import s6_servers, s6_args, s6_result

CHECKS = [
    ("s6_servers", s6_servers, 0.5),
    ("s6_args", s6_args, 0.5),
    ("s6_result", s6_result, 1.5),
]
