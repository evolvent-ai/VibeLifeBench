"""Stage 21 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s21_closeout_pending_no_unilateral = _mk(21, _S[21][0])

CHECKS = [
    ("s21_closeout_pending_no_unilateral", s21_closeout_pending_no_unilateral, 2.0),
]
