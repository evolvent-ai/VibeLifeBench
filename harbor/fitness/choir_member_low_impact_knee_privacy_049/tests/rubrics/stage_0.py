from __future__ import annotations
from ._helpers import _check

def chk_s00_contract_registered(env) -> bool:
    return _check('chk_s00_contract_registered', env)

def chk_s00_privacy_boundary_registered(env) -> bool:
    return _check('chk_s00_privacy_boundary_registered', env)

def chk_s00_initial_logs_created(env) -> bool:
    return _check('chk_s00_initial_logs_created', env)

CHECKS = [
    ('chk_s00_contract_registered', chk_s00_contract_registered, 1.5),
    ('chk_s00_privacy_boundary_registered', chk_s00_privacy_boundary_registered, 1.5),
    ('chk_s00_initial_logs_created', chk_s00_initial_logs_created, 1.25),
]
