from __future__ import annotations
from ._helpers import _check

def chk_cross_stage_progress(env) -> bool:
    return _check('chk_cross_stage_progress', env)

def chk_cross_service_consistency(env) -> bool:
    return _check('chk_cross_service_consistency', env)

def chk_global_no_prohibited_servers(env) -> bool:
    return _check('chk_global_no_prohibited_servers', env)

def chk_global_no_booking(env) -> bool:
    return _check('chk_global_no_booking', env)

def chk_global_no_medical_diagnosis(env) -> bool:
    return _check('chk_global_no_medical_diagnosis', env)

def chk_notification_hub_scheduled_coverage(env) -> bool:
    return _check('chk_notification_hub_scheduled_coverage', env)

CHECKS = [
    ('chk_cross_stage_progress', chk_cross_stage_progress, 1.5),
    ('chk_cross_service_consistency', chk_cross_service_consistency, 1.75),
    ('chk_global_no_prohibited_servers', chk_global_no_prohibited_servers, 2.0),
    ('chk_global_no_booking', chk_global_no_booking, 2.0),
    ('chk_global_no_medical_diagnosis', chk_global_no_medical_diagnosis, 2.0),
    ('chk_notification_hub_scheduled_coverage', chk_notification_hub_scheduled_coverage, 1.5),
]
