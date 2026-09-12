"""Stage 10 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s10_account_change_and_fee_refused = _mk(10, _S[10][0])

CHECKS = [
    ("s10_account_change_and_fee_refused", s10_account_change_and_fee_refused, 2.0),
]
