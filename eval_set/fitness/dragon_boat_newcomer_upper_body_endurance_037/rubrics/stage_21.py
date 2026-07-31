from __future__ import annotations
from ._helpers import _check

def chk_s21_sync_gap_safety_rules_persisted(env) -> bool:
    return _check('chk_s21_sync_gap_safety_rules_persisted', env)

def chk_s21_health_sync_gap_mutation(env) -> bool:
    return _check('chk_s21_health_sync_gap_mutation', env)

CHECKS = [
    ('chk_s21_sync_gap_safety_rules_persisted', chk_s21_sync_gap_safety_rules_persisted, 1.25),
    ('chk_s21_health_sync_gap_mutation', chk_s21_health_sync_gap_mutation, 1.5)
]
