"""Stage 9 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s09_curtain_withdrawal_detected = _mk(9, _S[9][0])

CHECKS = [
    ("s09_curtain_withdrawal_detected", s09_curtain_withdrawal_detected, 2.0),
]
