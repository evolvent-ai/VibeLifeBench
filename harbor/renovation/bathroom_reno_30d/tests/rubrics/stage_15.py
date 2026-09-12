"""Stage 15 checks, each backed by an independently named function in checks.py."""
from __future__ import annotations

from .checks import s15_servers, s15_result, s15_weather

CHECKS = [
    ("s15_servers", s15_servers, 0.5),
    ("s15_result", s15_result, 3.0),
    ("s15_weather", s15_weather, 2.5),
]
