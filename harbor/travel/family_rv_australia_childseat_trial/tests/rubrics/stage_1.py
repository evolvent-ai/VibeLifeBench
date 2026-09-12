from __future__ import annotations
from ._helpers import *

def s1_check_entry_requirements(env) -> bool:
    return _used_visa_entry_requirements(env, 1) and _check_text(env, 1, [['Australia', 'australia', 'au'], ['Australian visa', 'visa'], ['passport', 'passport'], ['documents', 'document']])

def s1_no_final_visa_judgment(env) -> bool:
    return _check_text(env, 1, [['cannot make', 'cannot', 'authority', 'final'], ['Australian visa', 'visa']], forbidden=['certain approval', 'guaranteed approval'])

def s1_calendar_visa_followup(env) -> bool:
    return _calendar_write_in_stage(env, 1) and _has_calendar(env, [['Australian visa', 'visa'], ['additional documents', 'follow', 'documents']])
CHECKS = [('s1_check_entry_requirements', s1_check_entry_requirements, 2.0), ('s1_no_final_visa_judgment', s1_no_final_visa_judgment, 2.0), ('s1_calendar_visa_followup', s1_calendar_visa_followup, 1.5)]
