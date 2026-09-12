"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

def s04_sensitive_sources_mapped(env):
    return _mk(4, _S[4][0])(env)


def s04_public_materials_not_sensitive(env):
    return _mk(4, _S[4][1])(env)

CHECKS = [
    ('s04_sensitive_sources_mapped', s04_sensitive_sources_mapped, 1.5),
    ('s04_public_materials_not_sensitive', s04_public_materials_not_sensitive, 5.0),
]
