"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s19_correct_holds_created = _mk(19, _S[19][0])
s19_cart_ready_no_order = _mk(19, _S[19][1])

CHECKS = [
    ('s19_correct_holds_created', s19_correct_holds_created, 2.0),
    ('s19_cart_ready_no_order', s19_cart_ready_no_order, 1.5),
]
