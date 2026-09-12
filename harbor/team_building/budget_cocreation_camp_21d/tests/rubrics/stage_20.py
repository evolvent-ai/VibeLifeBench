"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s20_scheduled_scan_completed = _mk(20, _S[20][0])
s20_final_freshness_checked = _mk(20, _S[20][1])

CHECKS = [
    ('s20_scheduled_scan_completed', s20_scheduled_scan_completed, 1.5),
    ('s20_final_freshness_checked', s20_final_freshness_checked, 1.5),
]
