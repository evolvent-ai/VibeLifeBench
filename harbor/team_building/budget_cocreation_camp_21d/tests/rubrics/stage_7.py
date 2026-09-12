"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s07_lunch_accessibility_checked = _mk(7, _S[7][0])
s07_dietary_constraints_logged = _mk(7, _S[7][1])

CHECKS = [
    ('s07_lunch_accessibility_checked', s07_lunch_accessibility_checked, 1.5),
    ('s07_dietary_constraints_logged', s07_dietary_constraints_logged, 1.25),
]
