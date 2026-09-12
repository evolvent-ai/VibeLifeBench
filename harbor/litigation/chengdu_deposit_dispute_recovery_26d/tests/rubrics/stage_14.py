"""Stage 14 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s14_evidence_package_assembled = _mk(14, _S[14][0])

CHECKS = [
    ("s14_evidence_package_assembled", s14_evidence_package_assembled, 1.25),
]
