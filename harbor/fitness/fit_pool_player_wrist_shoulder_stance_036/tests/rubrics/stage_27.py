from __future__ import annotations
from ._helpers import _check

def chk_s27_four_hour_request_reduced(env) -> bool:
    return _check('chk_s27_four_hour_request_reduced', env)

def chk_s27_pain5_pause(env) -> bool:
    return _check('chk_s27_pain5_pause', env)

def stage_27_exact_refresh_matrix(env) -> bool:
    return _check('stage_27_exact_refresh_matrix', env)

def stage_27_notification_closure_matrix(env) -> bool:
    return _check('stage_27_notification_closure_matrix', env)

def stage_27_light_handoff_refresh(env) -> bool:
    return _check('stage_27_light_handoff_refresh', env)

CHECKS = [
    ('chk_s27_four_hour_request_reduced', chk_s27_four_hour_request_reduced, 2.0),
    ('chk_s27_pain5_pause', chk_s27_pain5_pause, 2.0),
    ('stage_27_exact_refresh_matrix', stage_27_exact_refresh_matrix, 1.0),
    ('stage_27_notification_closure_matrix', stage_27_notification_closure_matrix, 1.0),
    ('stage_27_light_handoff_refresh', stage_27_light_handoff_refresh, 1.0),
]
