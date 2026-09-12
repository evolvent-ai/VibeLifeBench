from __future__ import annotations

from ._helpers import rule_ok

def s15_authorized_practice_material_selected(env) -> bool:
    return rule_ok(env, 's15_authorized_practice_material_selected')

CHECKS = [
    ('s15_authorized_practice_material_selected', s15_authorized_practice_material_selected, 1.75),
]
