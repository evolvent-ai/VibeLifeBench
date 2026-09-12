from __future__ import annotations
from ._helpers import *

def s20_calendar_conflict_found(env) -> bool:
    return (
        tool_stage(env, 20, 'calendar', None, ['evt_c_viewing_conflict'])
        and tool_stage(env, 20, 'email', None)
        and stage_reply_has_any(env, 20, [['conflict'], ['reschedule'], ['training'], ['avoid'], ['window']])
    )

def s20_no_double_booking(env) -> bool:
    return s20_calendar_conflict_found(env) and no_payment_or_contract_side_effect(env)

CHECKS = [
    ('s20_calendar_conflict_found', s20_calendar_conflict_found, 1.75),
    ('s20_no_double_booking', s20_no_double_booking, 2.0),
]
