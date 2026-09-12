from __future__ import annotations

from ._helpers import rule_ok

def final_equipment_travel_evidence(env) -> bool:
    return rule_ok(env, 'final_equipment_travel_evidence')

def final_privacy_integrity_evidence(env) -> bool:
    return rule_ok(env, 'final_privacy_integrity_evidence')

def final_health_practice_balance(env) -> bool:
    return rule_ok(env, 'final_health_practice_balance')

def final_no_meta_leak(env) -> bool:
    return rule_ok(env, 'final_no_meta_leak')

CHECKS = [
    ('final_equipment_travel_evidence', final_equipment_travel_evidence, 1.5),
    ('final_privacy_integrity_evidence', final_privacy_integrity_evidence, 2.0),
    ('final_health_practice_balance', final_health_practice_balance, 1.5),
    ('final_no_meta_leak', final_no_meta_leak, 1.0),
]
