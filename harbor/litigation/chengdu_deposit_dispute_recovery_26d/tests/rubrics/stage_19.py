"""Stage 19 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s19_risk_register_complete = _mk(19, _S[19][0])

CHECKS = [
    ("s19_risk_register_complete", s19_risk_register_complete, 1.5),
]
