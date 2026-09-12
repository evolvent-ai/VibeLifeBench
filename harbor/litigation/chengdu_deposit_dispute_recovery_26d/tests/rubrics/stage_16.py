"""Stage 16 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s16_offer_4800_not_accepted = _mk(16, _S[16][0])
s16_glass_inflation_rejected = _mk(16, _S[16][1])

CHECKS = [
    ("s16_offer_4800_not_accepted", s16_offer_4800_not_accepted, 2.0),
    ("s16_glass_inflation_rejected", s16_glass_inflation_rejected, 2.0),
]
