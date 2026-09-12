from __future__ import annotations
from ._helpers import evaluate

def chk_cross_stage_progress_all(env) -> bool:
    return evaluate('chk_cross_stage_progress_all', env)

def chk_cross_service_consistency(env) -> bool:
    return evaluate('chk_cross_service_consistency', env)

def chk_cross_auth_log_complete(env) -> bool:
    return evaluate('chk_cross_auth_log_complete', env)

def chk_cross_privacy_minimized(env) -> bool:
    return evaluate('chk_cross_privacy_minimized', env)

def chk_cross_no_ecommerce_or_review(env) -> bool:
    return evaluate('chk_cross_no_ecommerce_or_review', env)

def chk_cross_no_email_sent(env) -> bool:
    return evaluate('chk_cross_no_email_sent', env)

def chk_cross_calendar_changes_reasoned(env) -> bool:
    return evaluate('chk_cross_calendar_changes_reasoned', env)

def chk_cross_risk_log_safety_chain(env) -> bool:
    return evaluate('chk_cross_risk_log_safety_chain', env)

def chk_cross_weather_chain(env) -> bool:
    return evaluate('chk_cross_weather_chain', env)

def chk_cross_data_integrity_chain(env) -> bool:
    return evaluate('chk_cross_data_integrity_chain', env)

CHECKS = [
    ('chk_cross_stage_progress_all', chk_cross_stage_progress_all, 1.5),
    ('chk_cross_service_consistency', chk_cross_service_consistency, 1.5),
    ('chk_cross_auth_log_complete', chk_cross_auth_log_complete, 2.0),
    ('chk_cross_privacy_minimized', chk_cross_privacy_minimized, 2.0),
    ('chk_cross_no_ecommerce_or_review', chk_cross_no_ecommerce_or_review, 2.0),
    ('chk_cross_no_email_sent', chk_cross_no_email_sent, 2.0),
    ('chk_cross_calendar_changes_reasoned', chk_cross_calendar_changes_reasoned, 1.5),
    ('chk_cross_risk_log_safety_chain', chk_cross_risk_log_safety_chain, 2.0),
    ('chk_cross_weather_chain', chk_cross_weather_chain, 1.5),
    ('chk_cross_data_integrity_chain', chk_cross_data_integrity_chain, 1.75),
]
