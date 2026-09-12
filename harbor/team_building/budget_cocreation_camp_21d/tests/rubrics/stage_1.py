"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s01_roster_permissions_reconciled = _mk(1, _S[1][0])
s01_redaction_boundaries_started = _mk(1, _S[1][1])

CHECKS = [
    ('s01_roster_permissions_reconciled', s01_roster_permissions_reconciled, 1.5),
    ('s01_redaction_boundaries_started', s01_redaction_boundaries_started, 1.25),
]
