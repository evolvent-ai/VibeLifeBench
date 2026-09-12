"""Stage 12 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s12_distractor_isolation_502_only = _mk(12, _S[12][0])

CHECKS = [
    ("s12_distractor_isolation_502_only", s12_distractor_isolation_502_only, 2.0),
]
