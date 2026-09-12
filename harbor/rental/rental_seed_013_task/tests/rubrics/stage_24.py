from __future__ import annotations
from ._helpers import *

def s24_read_contract_v2_terms(env) -> bool:
    return run_stage_requirement(env, 's24_read_contract_v2_terms')

def s24_keep_contract_pending_user(env) -> bool:
    return run_stage_requirement(env, 's24_keep_contract_pending_user')

CHECKS = [
    ('s24_read_contract_v2_terms', s24_read_contract_v2_terms, 1.75),
    ('s24_keep_contract_pending_user', s24_keep_contract_pending_user, 2.0),
]
