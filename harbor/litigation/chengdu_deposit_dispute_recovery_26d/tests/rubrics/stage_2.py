"""Stage 2 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s02_movein_inspection_logged = _mk(2, _S[2][0])

CHECKS = [
    ("s02_movein_inspection_logged", s02_movein_inspection_logged, 1.25),
]
