"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s10_latest_budget_cap_used = _mk(10, _S[10][0])
s10_old_cap_superseded = _mk(10, _S[10][1])

CHECKS = [
    ('s10_latest_budget_cap_used', s10_latest_budget_cap_used, 1.75),
    ('s10_old_cap_superseded', s10_old_cap_superseded, 1.25),
]
