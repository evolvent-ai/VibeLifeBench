"""Stage 5 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s05_statutes_checked_and_logged = _mk(5, _S[5][0])

CHECKS = [
    ("s05_statutes_checked_and_logged", s05_statutes_checked_and_logged, 1.25),
]
