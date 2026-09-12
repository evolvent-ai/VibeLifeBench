from __future__ import annotations
from ._helpers import _check

def chk_s13_shoulder_pain_downgrade(env) -> bool:
    return _check('chk_s13_shoulder_pain_downgrade', env)

def chk_s13_pain_professional_boundary(env) -> bool:
    return _check('chk_s13_pain_professional_boundary', env)

def chk_s13_health_calendar_deload_light(env) -> bool:
    return _check('chk_s13_health_calendar_deload_light', env)

CHECKS = [
    ('chk_s13_shoulder_pain_downgrade', chk_s13_shoulder_pain_downgrade, 2.0),
    ('chk_s13_pain_professional_boundary', chk_s13_pain_professional_boundary, 1.5),
    ('chk_s13_health_calendar_deload_light', chk_s13_health_calendar_deload_light, 1.0)
]
