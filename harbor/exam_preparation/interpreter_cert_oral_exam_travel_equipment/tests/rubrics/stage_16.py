from __future__ import annotations

from ._helpers import rule_ok

def s16_equipment_delivered_check(env) -> bool:
    return rule_ok(env, 's16_equipment_delivered_check')

CHECKS = [
    ('s16_equipment_delivered_check', s16_equipment_delivered_check, 1.5),
]
