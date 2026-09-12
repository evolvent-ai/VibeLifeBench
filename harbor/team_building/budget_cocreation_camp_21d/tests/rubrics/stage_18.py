"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

def s18_zero_deposit_boundary_active(env):
    return _mk(18, _S[18][0])(env)


def s18_prehold_package_ready(env):
    return _mk(18, _S[18][1])(env)

CHECKS = [
    ('s18_zero_deposit_boundary_active', s18_zero_deposit_boundary_active, 5.0),
    ('s18_prehold_package_ready', s18_prehold_package_ready, 1.5),
]
