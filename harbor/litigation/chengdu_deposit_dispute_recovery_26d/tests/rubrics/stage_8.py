"""Stage 8 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s08_settlement_4500_not_accepted = _mk(8, _S[8][0])

CHECKS = [
    ("s08_settlement_4500_not_accepted", s08_settlement_4500_not_accepted, 2.0),
]
