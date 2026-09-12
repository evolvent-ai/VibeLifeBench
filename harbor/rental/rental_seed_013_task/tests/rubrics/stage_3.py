from __future__ import annotations
from ._helpers import *

def s3_check_office_a_commutes(env) -> bool:
    return run_stage_requirement(env, 's3_check_office_a_commutes')

def s3_create_budget_and_monitor(env) -> bool:
    return run_stage_requirement(env, 's3_create_budget_and_monitor')

CHECKS = [
    ('s3_check_office_a_commutes', s3_check_office_a_commutes, 1.5),
    ('s3_create_budget_and_monitor', s3_create_budget_and_monitor, 1.25),
]
