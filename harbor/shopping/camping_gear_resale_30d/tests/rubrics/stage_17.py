"""Stage 17 checks; each check is an independently named function in checks.py."""
from __future__ import annotations

from .checks import s17_platform, s17_confirm, s17_no_bad

CHECKS = [
    ("s17_platform", s17_platform, 2.0),
    ("s17_confirm", s17_confirm, 2.0),
    ("s17_no_bad", s17_no_bad, 0.5),
]
