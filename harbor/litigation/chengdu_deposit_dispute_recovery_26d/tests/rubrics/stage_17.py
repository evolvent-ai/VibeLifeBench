"""Stage 17 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s17_countdown_confirmed_dispute_filed = _mk(17, _S[17][0])

CHECKS = [
    ("s17_countdown_confirmed_dispute_filed", s17_countdown_confirmed_dispute_filed, 1.0),
]
