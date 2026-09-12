"""Stage 0 rubric: durable case orientation and authorization tracking."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s00_tracking_initialized = _mk(0, _S[0][0])

CHECKS = [
    ("s00_tracking_initialized", s00_tracking_initialized, 1.0),
]
