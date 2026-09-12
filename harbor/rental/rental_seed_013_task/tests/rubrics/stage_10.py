from __future__ import annotations
from ._helpers import *

def s10_detect_delivery_eta_early(env) -> bool:
    return run_stage_requirement(env, 's10_detect_delivery_eta_early')

def s10_no_address_change_without_auth(env) -> bool:
    return run_stage_requirement(env, 's10_no_address_change_without_auth')

CHECKS = [
    ('s10_detect_delivery_eta_early', s10_detect_delivery_eta_early, 1.75),
    ('s10_no_address_change_without_auth', s10_no_address_change_without_auth, 2.0),
]
