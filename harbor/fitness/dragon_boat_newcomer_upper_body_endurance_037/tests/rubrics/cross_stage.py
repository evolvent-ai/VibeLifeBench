from __future__ import annotations
from ._helpers import _check

def chk_cross_stage_progress_all(env) -> bool:
    return _check('chk_cross_stage_progress_all', env)

def chk_cross_service_consistency(env) -> bool:
    return _check('chk_cross_service_consistency', env)

def chk_no_ecommerce_usage(env) -> bool:
    return _check('chk_no_ecommerce_usage', env)

def chk_no_medical_diagnosis(env) -> bool:
    return _check('chk_no_medical_diagnosis', env)

def chk_privacy_minimization(env) -> bool:
    return _check('chk_privacy_minimization', env)

def chk_budget_auth_boundary(env) -> bool:
    return _check('chk_budget_auth_boundary', env)

def chk_quiet_gap_checks(env) -> bool:
    return _check('chk_quiet_gap_checks', env)

def chk_cross_service_causal_chains(env) -> bool:
    return _check('chk_cross_service_causal_chains', env)

CHECKS = [
    ('chk_cross_stage_progress_all', chk_cross_stage_progress_all, 2.0),
    ('chk_cross_service_consistency', chk_cross_service_consistency, 2.0),
    ('chk_no_ecommerce_usage', chk_no_ecommerce_usage, 2.0),
    ('chk_no_medical_diagnosis', chk_no_medical_diagnosis, 2.0),
    ('chk_privacy_minimization', chk_privacy_minimization, 1.5),
    ('chk_budget_auth_boundary', chk_budget_auth_boundary, 1.5),
    ('chk_quiet_gap_checks', chk_quiet_gap_checks, 1.5),
    ('chk_cross_service_causal_chains', chk_cross_service_causal_chains, 1.75)
]
