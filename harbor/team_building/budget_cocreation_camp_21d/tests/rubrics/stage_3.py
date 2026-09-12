"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s03_finance_email_read = _mk(3, _S[3][0])
s03_approval_log_initial = _mk(3, _S[3][1])

CHECKS = [
    ('s03_finance_email_read', s03_finance_email_read, 1.5),
    ('s03_approval_log_initial', s03_approval_log_initial, 1.25),
]
