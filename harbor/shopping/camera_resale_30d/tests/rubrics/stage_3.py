"""Stage 3 checks —  check  checks.py """
from __future__ import annotations

from .checks import s3_servers, s3_args, s3_result

CHECKS = [
    ("s3_servers", s3_servers, 0.5),
    ("s3_args", s3_args, 1.0),
    ("s3_result", s3_result, 2.0),
]
