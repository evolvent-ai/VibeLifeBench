from __future__ import annotations
from ._helpers import *

def s21_final_email_refresh(env) -> bool:
    return (
        tool_stage(env, 21, 'email', None)
        and tool_stage(env, 21, 'legal_search', None)
        and (
            (tool_stage(env, 21, 'notion', None, [C.LIST_B]) and notion_has_parts(env, [C.LIST_B]))
            or tool_stage(env, 21, 'calendar', None)
        )
    )

def s21_contract_questions_drafted(env) -> bool:
    return (
        (tool_stage(env, 21, 'email', 'save')
         or (draft_has_parts(env, ['lease']) and tool_stage(env, 21, 'legal_search', None)))
        and stage_reply_has_any(env, 21, [['no acceptance'], ['holding deposit'], ['authorization'], ['draft only'], ['pending']])
    )

CHECKS = [
    ('s21_final_email_refresh', s21_final_email_refresh, 1.5),
    ('s21_contract_questions_drafted', s21_contract_questions_drafted, 1.25),
]
