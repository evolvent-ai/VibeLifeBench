from __future__ import annotations
from ._helpers import *

def s25_refresh_all_core_services(env) -> bool:
    return run_stage_requirement(env, 's25_refresh_all_core_services')

def s25_create_final_five_part_review(env) -> bool:
    return run_stage_requirement(env, 's25_create_final_five_part_review')

CHECKS = [
    ('s25_refresh_all_core_services', s25_refresh_all_core_services, 1.75),
    ('s25_create_final_five_part_review', s25_create_final_five_part_review, 2.0),
]
