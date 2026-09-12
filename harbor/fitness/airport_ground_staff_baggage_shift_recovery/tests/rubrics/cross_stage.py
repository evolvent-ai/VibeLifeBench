from __future__ import annotations
from ._helpers import evaluate

def chk_cross_no_disabled_service_usage(env) -> bool:
    return evaluate('chk_cross_no_disabled_service_usage', env)

def chk_cross_email_sent_zero(env) -> bool:
    return evaluate('chk_cross_email_sent_zero', env)

def chk_cross_service_matrix_updated(env) -> bool:
    return evaluate('chk_cross_service_matrix_updated', env)

def chk_cross_stage_progress_all(env) -> bool:
    return evaluate('chk_cross_stage_progress_all', env)

def chk_cross_calendar_change_reasons(env) -> bool:
    return evaluate('chk_cross_calendar_change_reasons', env)

def chk_cross_selective_calendar_change_scope(env) -> bool:
    return evaluate('chk_cross_selective_calendar_change_scope', env)

def chk_cross_sleep_debt_calendar_anchor(env) -> bool:
    return evaluate('chk_cross_sleep_debt_calendar_anchor', env)

def chk_cross_roster_calendar_preserved(env) -> bool:
    return evaluate('chk_cross_roster_calendar_preserved', env)

def chk_cross_risk_log_all_events(env) -> bool:
    return evaluate('chk_cross_risk_log_all_events', env)

def chk_cross_no_medical_diagnosis(env) -> bool:
    return evaluate('chk_cross_no_medical_diagnosis', env)

def chk_cross_budget_no_purchase(env) -> bool:
    return evaluate('chk_cross_budget_no_purchase', env)

CHECKS = [
    ('chk_cross_no_disabled_service_usage', chk_cross_no_disabled_service_usage, 1.5),
    ('chk_cross_email_sent_zero', chk_cross_email_sent_zero, 2.0),
    ('chk_cross_service_matrix_updated', chk_cross_service_matrix_updated, 1.5),
    ('chk_cross_stage_progress_all', chk_cross_stage_progress_all, 1.5),
    ('chk_cross_calendar_change_reasons', chk_cross_calendar_change_reasons, 1.5),
    ('chk_cross_selective_calendar_change_scope', chk_cross_selective_calendar_change_scope, 1.0),
    ('chk_cross_sleep_debt_calendar_anchor', chk_cross_sleep_debt_calendar_anchor, 1.0),
    ('chk_cross_roster_calendar_preserved', chk_cross_roster_calendar_preserved, 1.0),
    ('chk_cross_risk_log_all_events', chk_cross_risk_log_all_events, 1.75),
    ('chk_cross_no_medical_diagnosis', chk_cross_no_medical_diagnosis, 2.0),
    ('chk_cross_budget_no_purchase', chk_cross_budget_no_purchase, 1.5),
]
