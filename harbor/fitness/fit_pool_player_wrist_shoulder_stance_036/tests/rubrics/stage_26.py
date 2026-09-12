from __future__ import annotations
from ._helpers import _check

def chk_s26_three_week_summary_integrated(env) -> bool:
    return _check('chk_s26_three_week_summary_integrated', env)

def stage_26_prefinal_three_service_refresh_light(env) -> bool:
    return _check('stage_26_prefinal_three_service_refresh_light', env)

CHECKS = [
    ('chk_s26_three_week_summary_integrated', chk_s26_three_week_summary_integrated, 1.25),
    ('stage_26_prefinal_three_service_refresh_light', stage_26_prefinal_three_service_refresh_light, 1.0),
]
