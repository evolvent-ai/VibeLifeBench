from __future__ import annotations
from ._helpers import _check

def chk_s09_heat_mutation_discovered(env) -> bool:
    return _check('chk_s09_heat_mutation_discovered', env)

def chk_s09_work_heat_replan(env) -> bool:
    return _check('chk_s09_work_heat_replan', env)

def chk_cb_s09_heat_recheck_floor(env) -> bool:
    return _check('chk_cb_s09_heat_recheck_floor', env)

def chk_cb_pro_s09_heat_calendar_bridge(env) -> bool:
    return _check('chk_cb_pro_s09_heat_calendar_bridge', env)

CHECKS = [
    ('chk_s09_heat_mutation_discovered', chk_s09_heat_mutation_discovered, 1.75),
    ('chk_s09_work_heat_replan', chk_s09_work_heat_replan, 1.25),
    ('chk_cb_s09_heat_recheck_floor', chk_cb_s09_heat_recheck_floor, 1.25),
    ('chk_cb_pro_s09_heat_calendar_bridge', chk_cb_pro_s09_heat_calendar_bridge, 1.0),
]
