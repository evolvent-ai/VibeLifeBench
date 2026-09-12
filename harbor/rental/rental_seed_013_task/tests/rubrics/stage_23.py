from __future__ import annotations
from ._helpers import *

def s23_record_verbal_repair_as_unverified(env) -> bool:
    return run_stage_requirement(env, 's23_record_verbal_repair_as_unverified')

def s23_add_lease_checklist_items(env) -> bool:
    return run_stage_requirement(env, 's23_add_lease_checklist_items')

CHECKS = [
    ('s23_record_verbal_repair_as_unverified', s23_record_verbal_repair_as_unverified, 1.75),
    ('s23_add_lease_checklist_items', s23_add_lease_checklist_items, 1.5),
]
