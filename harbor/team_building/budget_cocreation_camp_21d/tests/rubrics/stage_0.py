"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s00_control_files_started = _mk(0, _S[0][0])
s00_no_irreversible = _mk(0, _S[0][1])

CHECKS = [
    ('s00_control_files_started', s00_control_files_started, 1.25),
    ('s00_no_irreversible', s00_no_irreversible, 0.5),
]
