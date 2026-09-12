from __future__ import annotations

from ._helpers import rule_ok

def s07_scheduled_equipment_check(env) -> bool:
    return rule_ok(env, 's07_scheduled_equipment_check')

CHECKS = [
    ('s07_scheduled_equipment_check', s07_scheduled_equipment_check, 1.5),
]
