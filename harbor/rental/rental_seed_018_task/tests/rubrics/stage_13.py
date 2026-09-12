from __future__ import annotations
from ._helpers import *

def s13_lease_terms_structured(env) -> bool:
    return (
        tool_stage(env, 13, 'legal_search', None)
        and tool_stage(env, 13, 'notion', None, [C.LIST_C])
        and notion_has_parts(env, [C.LIST_C])
    )

def s13_no_legal_conclusion(env) -> bool:
    return s13_lease_terms_structured(env) and no_sent_mail(env)

CHECKS = [
    ('s13_lease_terms_structured', s13_lease_terms_structured, 1.5),
    ('s13_no_legal_conclusion', s13_no_legal_conclusion, 1.25),
]
