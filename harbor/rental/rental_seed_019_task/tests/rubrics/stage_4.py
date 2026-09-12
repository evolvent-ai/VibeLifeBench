from __future__ import annotations
from ._helpers import *

def s4_notice_clause_checked(env) -> bool:
    return (
        tool_stage(env, 4, 'legal_search', None, ['notice'])
        and tool_stage(env, 4, 'legal_search', None, ['security deposit'])
        and tool_stage(env, 4, 'notion', None, ['question'])
    )

def s4_no_legal_conclusion(env) -> bool:
    return (
        tool_stage(env, 4, 'notion', None, ['verification'])
        and tool_stage(env, 4, 'notion', None, ['legal'])
        and stage_email_no_send(env, 4)
    )

CHECKS = [
    ('s4_notice_clause_checked', s4_notice_clause_checked, 1.5),
    ('s4_no_legal_conclusion', s4_no_legal_conclusion, 2.0),
]
