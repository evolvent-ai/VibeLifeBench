"""Stage 1 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s01_lease_and_deposit_pulled = _mk(1, _S[1][0])
s01_deposit_amount_grounded_in_bank = _mk(1, _S[1][1])

CHECKS = [
    ("s01_lease_and_deposit_pulled", s01_lease_and_deposit_pulled, 1.25),
    ("s01_deposit_amount_grounded_in_bank", s01_deposit_amount_grounded_in_bank, 1.25),
]
