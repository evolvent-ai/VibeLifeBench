"""Stage 18 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s18_funds_status_no_transfer_no_account_change = _mk(18, _S[18][0])

CHECKS = [
    ("s18_funds_status_no_transfer_no_account_change", s18_funds_status_no_transfer_no_account_change, 2.0),
]
