"""Stage 20 checks — Each check is an independent named function from checks.py."""
from __future__ import annotations

from .checks import s20_servers, s20_result

CHECKS = [
    ("s20_servers", s20_servers, 0.5),
    ("s20_result", s20_result, 2.5),
]
