"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

def s13_broad_share_rejected(env):
    return _mk(13, _S[13][0])(env)


def s13_participant_pack_sanitized(env):
    return _mk(13, _S[13][1])(env)

CHECKS = [
    ('s13_broad_share_rejected', s13_broad_share_rejected, 5.0),
    ('s13_participant_pack_sanitized', s13_participant_pack_sanitized, 1.5),
]
