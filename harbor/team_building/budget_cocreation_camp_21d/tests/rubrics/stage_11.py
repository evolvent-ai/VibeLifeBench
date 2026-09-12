"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s11_vendor_discount_rechecked = _mk(11, _S[11][0])
_s11_ledger_recomputed = _mk(11, _S[11][1])


def s11_ledger_recomputed(env):
    return _s11_ledger_recomputed(env)

CHECKS = [
    ('s11_vendor_discount_rechecked', s11_vendor_discount_rechecked, 1.75),
    ('s11_ledger_recomputed', s11_ledger_recomputed, 1.5),
]
