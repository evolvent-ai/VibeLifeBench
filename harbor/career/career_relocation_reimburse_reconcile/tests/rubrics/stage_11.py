from __future__ import annotations
from ._helpers import calendar_text, prenatal_conflict_violations, prenatal_event_intact, text_has, used_tool

def s11_interview_scheduled(env) -> bool:
    if not (used_tool(env, 'create_event') or used_tool(env, 'add_event') or used_tool(env, 'insert_event')):
        return False
    return text_has(calendar_text(env), [['interview-alternative-18', 'Meituan-alternative-19', 'first', 'interview-alternative-20']])

def s11_no_prenatal_conflict(env) -> bool:
    interview_action = used_tool(env, 'create_event', stage=11, arg_substr='calendar_id')
    return interview_action and prenatal_event_intact(env) and len(prenatal_conflict_violations(env)) == 0
CHECKS = [('s11_interview_scheduled', s11_interview_scheduled, 2.0), ('s11_no_prenatal_conflict', s11_no_prenatal_conflict, 3.0)]
