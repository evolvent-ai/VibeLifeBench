from __future__ import annotations
from ._helpers import _check

def chk_s25_final_notice_auth_equipment(env) -> bool:
    return _check('chk_s25_final_notice_auth_equipment', env)

def chk_s25_precamp_integrated_check(env) -> bool:
    return _check('chk_s25_precamp_integrated_check', env)

def chk_cb_s25_precamp_refresh_floor(env) -> bool:
    return _check('chk_cb_s25_precamp_refresh_floor', env)

def chk_cb_pro_s25_auth_equipment_refresh(env) -> bool:
    return _check('chk_cb_pro_s25_auth_equipment_refresh', env)

def chk_cb_pro_s25_notice_equipment_bridge(env) -> bool:
    return _check('chk_cb_pro_s25_notice_equipment_bridge', env)

def chk_cb_pro_s25_health_calendar_bridge(env) -> bool:
    return _check('chk_cb_pro_s25_health_calendar_bridge', env)

def chk_cb_pro_s25_weather_health_bridge(env) -> bool:
    return _check('chk_cb_pro_s25_weather_health_bridge', env)

CHECKS = [
    ('chk_s25_final_notice_auth_equipment', chk_s25_final_notice_auth_equipment, 1.75),
    ('chk_s25_precamp_integrated_check', chk_s25_precamp_integrated_check, 1.5),
    ('chk_cb_s25_precamp_refresh_floor', chk_cb_s25_precamp_refresh_floor, 1.25),
    ('chk_cb_pro_s25_auth_equipment_refresh', chk_cb_pro_s25_auth_equipment_refresh, 1.25),
    ('chk_cb_pro_s25_notice_equipment_bridge', chk_cb_pro_s25_notice_equipment_bridge, 1.0),
    ('chk_cb_pro_s25_health_calendar_bridge', chk_cb_pro_s25_health_calendar_bridge, 1.0),
    ('chk_cb_pro_s25_weather_health_bridge', chk_cb_pro_s25_weather_health_bridge, 1.0),
]
