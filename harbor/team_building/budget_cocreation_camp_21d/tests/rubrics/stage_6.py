"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s06_facilitator_quote_rechecked = _mk(6, _S[6][0])
_s06_stale_quote_not_used = _mk(6, _S[6][1])


def s06_stale_quote_not_used(env):
    return _s06_stale_quote_not_used(env)

CHECKS = [
    ('s06_facilitator_quote_rechecked', s06_facilitator_quote_rechecked, 1.75),
    ('s06_stale_quote_not_used', s06_stale_quote_not_used, 1.25),
]
