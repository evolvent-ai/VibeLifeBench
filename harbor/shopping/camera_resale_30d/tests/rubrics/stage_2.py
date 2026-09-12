"""Stage 2 checks —  check  checks.py """
from __future__ import annotations

from .checks import s2_servers, s2_args, s2_result, s2_options

CHECKS = [
    ("s2_servers", s2_servers, 0.5),
    ("s2_args", s2_args, 1.0),
    ("s2_result", s2_result, 2.0),
    ("s2_options", s2_options, 2.0),
]
