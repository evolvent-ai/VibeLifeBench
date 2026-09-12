from __future__ import annotations
from ._helpers import evaluate

def chk_s01_baseline_services_read(env) -> bool:
    return evaluate('chk_s01_baseline_services_read', env)

def chk_s01_three_tier_template(env) -> bool:
    return evaluate('chk_s01_three_tier_template', env)

def chk_s01_tier_labels_persisted(env) -> bool:
    return evaluate('chk_s01_tier_labels_persisted', env)

def chk_s01_safety_downgrade_fields(env) -> bool:
    return evaluate('chk_s01_safety_downgrade_fields', env)

CHECKS = [
    ('chk_s01_baseline_services_read', chk_s01_baseline_services_read, 1.25),
    ('chk_s01_three_tier_template', chk_s01_three_tier_template, 1.5),
    ('chk_s01_tier_labels_persisted', chk_s01_tier_labels_persisted, 1.0),
    ('chk_s01_safety_downgrade_fields', chk_s01_safety_downgrade_fields, 1.0),
]
