"""Stage 10 checks —  check  checks.py """
from __future__ import annotations

from .checks import s10_servers, s10_args, s10_result, s10_no_bad

CHECKS = [
    ("s10_servers", s10_servers, 0.5),
    ("s10_args", s10_args, 0.5),
    ("s10_result", s10_result, 3.0),
    ("s10_no_bad", s10_no_bad, 0.5),
]
