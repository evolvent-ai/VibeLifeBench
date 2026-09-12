from __future__ import annotations
from ._helpers import _check

def chk_budget_within_3000(env) -> bool:
    return _check('chk_budget_within_3000', env)

def chk_notion_hub_complete(env) -> bool:
    return _check('chk_notion_hub_complete', env)

def chk_weather_venue_log_complete(env) -> bool:
    return _check('chk_weather_venue_log_complete', env)

def chk_risk_log_complete(env) -> bool:
    return _check('chk_risk_log_complete', env)

def chk_auth_log_complete(env) -> bool:
    return _check('chk_auth_log_complete', env)

def chk_final_latest_refresh_before_review(env) -> bool:
    return _check('chk_final_latest_refresh_before_review', env)

CHECKS = [
    ('chk_budget_within_3000', chk_budget_within_3000, 1.25),
    ('chk_notion_hub_complete', chk_notion_hub_complete, 1.25),
    ('chk_weather_venue_log_complete', chk_weather_venue_log_complete, 1.25),
    ('chk_risk_log_complete', chk_risk_log_complete, 1.5),
    ('chk_auth_log_complete', chk_auth_log_complete, 1.25),
    ('chk_final_latest_refresh_before_review', chk_final_latest_refresh_before_review, 1.5),
]
