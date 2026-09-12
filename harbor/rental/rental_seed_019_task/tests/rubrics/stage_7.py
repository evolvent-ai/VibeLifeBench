from __future__ import annotations
from ._helpers import *

def s7_deposit_risk_logged(env) -> bool:
    return (
        tool_stage(env, 7, 'notion', None, ['security deposit'])
        and tool_stage(env, 7, 'notion', None, ['damp mark'])
        and workspace_file_has_groups(env, 'DEPOSIT_RISK_LOG.md', [('security deposit',), ('damp mark',), ('status',)])
    )

def s7_draft_questions_prepared(env) -> bool:
    return (
        stage_email_draft(env, 7, [('security deposit', 'damp mark'), ('question', 'verification')])
        and stage_email_no_send(env, 7)
    )

CHECKS = [
    ('s7_deposit_risk_logged', s7_deposit_risk_logged, 1.5),
    ('s7_draft_questions_prepared', s7_draft_questions_prepared, 1.25),
]
