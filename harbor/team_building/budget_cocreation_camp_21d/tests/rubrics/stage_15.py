"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s15_material_stock_rechecked = _mk(15, _S[15][0])
s15_cart_still_no_order = _mk(15, _S[15][1])

CHECKS = [
    ('s15_material_stock_rechecked', s15_material_stock_rechecked, 1.75),
    ('s15_cart_still_no_order', s15_cart_still_no_order, 1.0),
]
