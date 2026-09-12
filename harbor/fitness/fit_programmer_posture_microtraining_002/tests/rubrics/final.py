from __future__ import annotations
from ._helpers import _check

def chk_final_review_evidence(env) -> bool:
    return _check('chk_final_review_evidence', env)

def chk_final_auth_statement(env) -> bool:
    return _check('chk_final_auth_statement', env)

def chk_final_next_cycle(env) -> bool:
    return _check('chk_final_next_cycle', env)

def chk_final_diff_latest_refresh_before_review(env) -> bool:
    return _check('chk_final_diff_latest_refresh_before_review', env)

def chk_final_diff_open_risk_handoff(env) -> bool:
    return _check('chk_final_diff_open_risk_handoff', env)

def chk_final_diff_asset_readback_lite(env) -> bool:
    return _check('chk_final_diff_asset_readback_lite', env)

CHECKS = [
    ('chk_final_review_evidence', chk_final_review_evidence, 1.75),
    ('chk_final_auth_statement', chk_final_auth_statement, 2),
    ('chk_final_next_cycle', chk_final_next_cycle, 1.5),
    ('chk_final_diff_latest_refresh_before_review', chk_final_diff_latest_refresh_before_review, 1.5),
    ('chk_final_diff_open_risk_handoff', chk_final_diff_open_risk_handoff, 1.25),
    ('chk_final_diff_asset_readback_lite', chk_final_diff_asset_readback_lite, 1.0),
]
