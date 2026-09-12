from __future__ import annotations
from ._helpers import *

def s19_schedule_buffer_checked(env) -> bool:
    return (
        tool_stage(env, 19, 'calendar', None)
        and tool_stage(env, 19, 'maps', None, [C.HOSPITAL])
        and stage_reply_has_any(env, 19, [['verified'], ['pending'], ['documents'], ['lease'], ['retained']])
    )

def s19_no_external_appointment(env) -> bool:
    return s19_schedule_buffer_checked(env) and len(viewings(env)) == 0

CHECKS = [
    ('s19_schedule_buffer_checked', s19_schedule_buffer_checked, 1.25),
    ('s19_no_external_appointment', s19_no_external_appointment, 2.0),
]
