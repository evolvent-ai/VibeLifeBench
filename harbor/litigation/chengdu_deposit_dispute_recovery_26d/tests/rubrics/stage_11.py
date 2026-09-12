"""Stage 11 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s11_per_item_deduction_analysis = _mk(11, _S[11][0])
s11_deductible_set_reasoned = _mk(11, _S[11][1])

CHECKS = [
    ("s11_per_item_deduction_analysis", s11_per_item_deduction_analysis, 2.0),
    ("s11_deductible_set_reasoned", s11_deductible_set_reasoned, 1.5),
]
