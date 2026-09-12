"""Stage 12 checks — Each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s12_servers, s12_reject

CHECKS = [
    ("s12_servers", s12_servers, 0.5),
    ("s12_reject", s12_reject, 4.0),
]
