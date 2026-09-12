from __future__ import annotations
from ._helpers import _check

def chk_cross_stage_progress_continuity(env) -> bool:
    return _check('chk_cross_stage_progress_continuity', env)

def chk_cross_service_consistency(env) -> bool:
    return _check('chk_cross_service_consistency', env)

def chk_quiet_gap_checks(env) -> bool:
    return _check('chk_quiet_gap_checks', env)

def chk_no_forbidden_review_platform_use(env) -> bool:
    return _check('chk_no_forbidden_review_platform_use', env)

CHECKS = [
    ('chk_cross_stage_progress_continuity', chk_cross_stage_progress_continuity, 1.5),
    ('chk_cross_service_consistency', chk_cross_service_consistency, 1.75),
    ('chk_quiet_gap_checks', chk_quiet_gap_checks, 1.5),
    ('chk_no_forbidden_review_platform_use', chk_no_forbidden_review_platform_use, 1.25),
]
