from __future__ import annotations
from ._helpers import _check

def chk_s22_sync_gap_detected(env) -> bool:
    return _check('chk_s22_sync_gap_detected', env)

def chk_s22_missing_not_fabricated(env) -> bool:
    return _check('chk_s22_missing_not_fabricated', env)

def stage_22_data_quality_positive_action(env) -> bool:
    return _check('stage_22_data_quality_positive_action', env)

CHECKS = [
    ('chk_s22_sync_gap_detected', chk_s22_sync_gap_detected, 1.5),
    ('chk_s22_missing_not_fabricated', chk_s22_missing_not_fabricated, 2.0),
    ('stage_22_data_quality_positive_action', stage_22_data_quality_positive_action, 1.0),
]
