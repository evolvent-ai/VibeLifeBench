"""Stage 20 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s20_recommendation_unique_amount = _mk(20, _S[20][0])
s20_reserved_actions_flagged = _mk(20, _S[20][1])

CHECKS = [
    ("s20_recommendation_unique_amount", s20_recommendation_unique_amount, 1.5),
    ("s20_reserved_actions_flagged", s20_reserved_actions_flagged, 2.0),
]
