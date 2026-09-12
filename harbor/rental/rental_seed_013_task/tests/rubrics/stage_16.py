from __future__ import annotations
from ._helpers import *

def s16_detect_training_conflict(env) -> bool:
    return run_stage_requirement(env, 's16_detect_training_conflict')

def s16_draft_reschedule_without_sending(env) -> bool:
    return run_stage_requirement(env, 's16_draft_reschedule_without_sending')

CHECKS = [
    ('s16_detect_training_conflict', s16_detect_training_conflict, 1.5),
    ('s16_draft_reschedule_without_sending', s16_draft_reschedule_without_sending, 1.25),
]
