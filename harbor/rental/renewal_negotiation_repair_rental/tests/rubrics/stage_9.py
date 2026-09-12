from __future__ import annotations
from ._helpers import *

def s9_legal_contract_checklist(env) -> bool:
    return bool(
        tool_stage_group(env, 9, 'legal_search', None, [('rental',), ('deposit',), ('repair',)])
        and legal_source_has(env, ('rental',))
        and derived_stage_has(env, 9, ('contracting party', 'deposit', 'repair', 'payment route'), ('LEASE_CHECKLIST.md', 'RISK_LOG.md'))
    )

def s9_email_followup_draft(env) -> bool:
    return bool(
        tool_stage(env, 9, 'email', 'save', ('contracting party', 'deposit', 'repair'))
        and draft_has_parts(env, ('contracting party', 'deposit', 'repair'))
        and no_sent_mail(env)
    )

CHECKS = [
    ("s9_legal_contract_checklist", s9_legal_contract_checklist, 1.5),
    ("s9_email_followup_draft", s9_email_followup_draft, 1.25),
]
