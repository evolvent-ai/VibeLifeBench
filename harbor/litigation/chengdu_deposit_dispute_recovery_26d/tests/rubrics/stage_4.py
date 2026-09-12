"""Stage 4 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s04_repair_cleaning_quotes_logged = _mk(4, _S[4][0])

CHECKS = [
    ("s04_repair_cleaning_quotes_logged", s04_repair_cleaning_quotes_logged, 1.25),
]
