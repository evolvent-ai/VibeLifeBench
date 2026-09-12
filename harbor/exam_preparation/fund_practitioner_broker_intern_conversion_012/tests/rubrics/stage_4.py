from ._helpers import *

def s4_study_baseline_no_roadshow_conflict(env) -> bool:
    return h_s4_study_baseline_no_roadshow_conflict(env)

def s4_material_shortlist_started(env) -> bool:
    return h_s4_material_shortlist_started(env)

CHECKS = [
    ("s4_study_baseline_no_roadshow_conflict", s4_study_baseline_no_roadshow_conflict, 1.5),
    ("s4_material_shortlist_started", s4_material_shortlist_started, 1.25),
]
