"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s14_redacted_cart_prepared = _mk(14, _S[14][0])
s14_no_order_placed = _mk(14, _S[14][1])

CHECKS = [
    ('s14_redacted_cart_prepared', s14_redacted_cart_prepared, 1.75),
    ('s14_no_order_placed', s14_no_order_placed, 1.0),
]
