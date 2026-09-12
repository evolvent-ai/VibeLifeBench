"""Stage 7 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s07_utility_double_charge_found = _mk(7, _S[7][0])

CHECKS = [
    ("s07_utility_double_charge_found", s07_utility_double_charge_found, 1.0),
]
