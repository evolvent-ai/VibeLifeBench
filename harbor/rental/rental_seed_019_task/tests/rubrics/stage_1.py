from __future__ import annotations
from ._helpers import *

def s1_contract_email_reviewed(env) -> bool:
    return stage_read_email_ids(env, 1, ('1',)) and tool_stage(env, 1, 'email', 'read_email', ['thread_landlord_renewal'])

def s1_calendar_expiry_recorded(env) -> bool:
    return tool_stage(env, 1, 'calendar', None, ['2026-08-07'])

CHECKS = [
    ('s1_contract_email_reviewed', s1_contract_email_reviewed, 1.5),
    ('s1_calendar_expiry_recorded', s1_calendar_expiry_recorded, 1.25),
]
