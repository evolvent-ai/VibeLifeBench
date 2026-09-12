"""Stage 3 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s03_moveout_compare_logged = _mk(3, _S[3][0])

CHECKS = [
    ("s03_moveout_compare_logged", s03_moveout_compare_logged, 1.25),
]
