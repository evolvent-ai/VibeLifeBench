"""Stage 9 checks — Each check is an independent named function from checks.py."""
from __future__ import annotations

from .checks import s9_servers, s9_args, s9_result

CHECKS = [
    ("s9_servers", s9_servers, 0.5),
    ("s9_args", s9_args, 0.5),
    ("s9_result", s9_result, 2.5),
]
