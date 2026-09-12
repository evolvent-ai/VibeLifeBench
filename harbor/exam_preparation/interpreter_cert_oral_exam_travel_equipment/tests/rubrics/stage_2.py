from __future__ import annotations

from ._helpers import rule_ok

def s02_official_handbook_equipment(env) -> bool:
    return rule_ok(env, 's02_official_handbook_equipment')

def s02_equipment_check_window_logged(env) -> bool:
    return rule_ok(env, 's02_equipment_check_window_logged')

CHECKS = [
    ('s02_official_handbook_equipment', s02_official_handbook_equipment, 1.5),
    ('s02_equipment_check_window_logged', s02_equipment_check_window_logged, 1.25),
]
