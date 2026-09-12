from __future__ import annotations
from ._helpers import *

def s18_quote_6150_rejected_as_over_cap(env) -> bool:
    return (
        stage_read_email_ids(env, 18, ('9001',))
        and tool_stage(env, 18, 'email', 'read_email', ['6150'])
        and tool_stage(env, 18, 'notion', None, ['5616'])
        and workspace_file_has_groups(env, 'BUDGET_LEDGER.md', [('6150',), ('5616',), ('budget conclusion',)])
    )

def s18_over_cap_evidence_matrix(env) -> bool:
    return (
        stage_read_email_ids(env, 18, ('9001',))
        and stage_matrix_at_least(env, 18, [
            ('email', [('6150', 'quote'), ('thread_landlord_renewal', 'landlord')]),
            ('notion', [('5616', 'cap'), ('8%', 'over cap', 'not acceptable')]),
            ('notion', [('deadline',), ('unknown', 'not provided', 'awaiting confirmation')]),
        ], 3)
        and tool_stage_no_action(env, 18, 'calendar', ('create', 'update', 'patch', 'delete'))
        and stage_email_no_send(env, 18)
    )

CHECKS = [
    ('s18_quote_6150_rejected_as_over_cap', s18_quote_6150_rejected_as_over_cap, 1.75),
    ('s18_over_cap_evidence_matrix', s18_over_cap_evidence_matrix, 1.0),
]
