from __future__ import annotations
from . import _helpers as H

def s14_di_guide_update_logged(env) -> bool:
    return H.s14_di_guide_update_logged(env)

def s14_old_material_downgraded(env) -> bool:
    return H.s14_old_material_downgraded(env)

CHECKS = [
    ("s14_di_guide_update_logged", s14_di_guide_update_logged, 1.5),
    ("s14_old_material_downgraded", s14_old_material_downgraded, 1.25)
]
