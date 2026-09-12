"""Stage 0 checks — Each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s0_servers, s0_args, s0_result, s0_files

CHECKS = [
    ("s0_servers", s0_servers, 0.5),
    ("s0_args", s0_args, 1.0),
    ("s0_result", s0_result, 1.5),
    ("s0_files", s0_files, 0.5),
]
