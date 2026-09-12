"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s12_venue_capacity_rechecked = _mk(12, _S[12][0])
_s12_valid_venue_kept = _mk(12, _S[12][1])


def s12_valid_venue_kept(env):
    return _s12_valid_venue_kept(env)

CHECKS = [
    ('s12_venue_capacity_rechecked', s12_venue_capacity_rechecked, 1.75),
    ('s12_valid_venue_kept', s12_valid_venue_kept, 1.25),
]
