"""Stage 6 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s06_wall_raise_detected = _mk(6, _S[6][0])
s06_dispute_status_rechecked = _mk(6, _S[6][1])

CHECKS = [
    ("s06_wall_raise_detected", s06_wall_raise_detected, 1.0),
    ("s06_dispute_status_rechecked", s06_dispute_status_rechecked, 1.0),
]
