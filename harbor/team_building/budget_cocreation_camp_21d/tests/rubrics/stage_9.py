"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s09_roster_delta_rechecked = _mk(9, _S[9][0])
s09_permissions_after_delta = _mk(9, _S[9][1])

CHECKS = [
    ('s09_roster_delta_rechecked', s09_roster_delta_rechecked, 1.5),
    ('s09_permissions_after_delta', s09_permissions_after_delta, 1.25),
]
