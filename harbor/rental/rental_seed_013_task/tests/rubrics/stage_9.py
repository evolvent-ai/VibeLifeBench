from __future__ import annotations
from ._helpers import *

def s9_triage_notifications(env) -> bool:
    return run_stage_requirement(env, 's9_triage_notifications')

def s9_preserve_onboarding_buffer(env) -> bool:
    return run_stage_requirement(env, 's9_preserve_onboarding_buffer')

CHECKS = [
    ('s9_triage_notifications', s9_triage_notifications, 1.0),
    ('s9_preserve_onboarding_buffer', s9_preserve_onboarding_buffer, 1.0),
]
