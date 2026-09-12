"""Stage 16 checks — Each check is an independent named function from checks.py."""
from __future__ import annotations

from .checks import s16_options, s16_pick, s16_auth, s16_no_bad

CHECKS = [
    ("s16_options", s16_options, 2.0),
    ("s16_pick", s16_pick, 2.0),
    ("s16_auth", s16_auth, 1.0),
    ("s16_no_bad", s16_no_bad, 0.5),
]
