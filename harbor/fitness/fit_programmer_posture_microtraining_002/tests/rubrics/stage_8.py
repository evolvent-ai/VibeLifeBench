from __future__ import annotations
from ._helpers import _check

def chk_s08_equipment_screening(env) -> bool:
    return _check('chk_s08_equipment_screening', env)

CHECKS = [
    ('chk_s08_equipment_screening', chk_s08_equipment_screening, 1.75),
]
