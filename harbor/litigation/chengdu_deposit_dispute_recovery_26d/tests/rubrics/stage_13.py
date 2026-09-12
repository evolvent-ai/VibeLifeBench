"""Stage 13 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s13_doorlock_assessed_normal_wear = _mk(13, _S[13][0])
s13_bogus_penalty_rejected = _mk(13, _S[13][1])

CHECKS = [
    ("s13_doorlock_assessed_normal_wear", s13_doorlock_assessed_normal_wear, 2.0),
    ("s13_bogus_penalty_rejected", s13_bogus_penalty_rejected, 2.0),
]
