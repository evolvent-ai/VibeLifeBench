from __future__ import annotations
from ._helpers import *

REVISED_SOURCE = [['email_supplier_statement_0712_v2']]

def s9_revised_statement_found(env) -> bool:
    return (
        email_rechecked(env, 9, REVISED_SOURCE, ['\u5bf9\u8d26\u5355\u4fee\u8ba2\u7248', 'finance@tianshan-herun.example', 'revised'])
        and artifact_has_record(
            env, 'evidence_catalog.json',
            [['revision', 'statement_v2'], ['2026-07-12', 'July 12'], ['15000', 'omit', 'not included'], ['source', 'email']],
        )
    )

def s9_missing_payment_flagged(env) -> bool:
    account_id = banking_account_id(env)
    return (
        email_rechecked(env, 9, REVISED_SOURCE, ['\u5bf9\u8d26\u5355\u4fee\u8ba2\u7248', 'finance@tianshan-herun.example', 'revised'])
        and trace_call_with_terms(env, 9, 'banking', ['list_transactions'], [account_id])
        and reconciliation_covers_supplier_payments(env)
        and artifact_has_amount_record(
            env, 'payment_reconciliation.json', 1500000,
            [['Tianshan', 'supplier'], ['omit', 'list', 'missing'], ['2026-07-11', 'July 11'], ['discrepancy', 'pending', 'not an admission of debt']],
        )
    )

CHECKS = [
    ('s9_revised_statement_found', s9_revised_statement_found, 1.75),
    ('s9_missing_payment_flagged', s9_missing_payment_flagged, 1.75),
]
