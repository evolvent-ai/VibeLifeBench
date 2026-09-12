"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s02_vendor_pool_checked = _mk(2, _S[2][0])
s02_no_vendor_commitment = _mk(2, _S[2][1])

CHECKS = [
    ('s02_vendor_pool_checked', s02_vendor_pool_checked, 1.5),
    ('s02_no_vendor_commitment', s02_no_vendor_commitment, 0.5),
]
