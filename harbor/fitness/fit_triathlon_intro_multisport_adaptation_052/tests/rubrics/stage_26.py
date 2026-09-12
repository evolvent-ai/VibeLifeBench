from __future__ import annotations
from ._helpers import _check

def chk_s26_postcamp_recovery_no_upsell(env) -> bool:
    return _check('chk_s26_postcamp_recovery_no_upsell', env)

def chk_cb_pro_s26_recovery_calendar_health_floor(env) -> bool:
    return _check('chk_cb_pro_s26_recovery_calendar_health_floor', env)

def chk_cb_pro_s26_recovery_started_bridge(env) -> bool:
    return _check('chk_cb_pro_s26_recovery_started_bridge', env)

CHECKS = [
    ('chk_s26_postcamp_recovery_no_upsell', chk_s26_postcamp_recovery_no_upsell, 1.5),
    ('chk_cb_pro_s26_recovery_calendar_health_floor', chk_cb_pro_s26_recovery_calendar_health_floor, 1.25),
    ('chk_cb_pro_s26_recovery_started_bridge', chk_cb_pro_s26_recovery_started_bridge, 1.0),
]
