from __future__ import annotations
from ._helpers import *

def s23_invoice_budget_reconcile(env) -> bool:
    return used(env, 23, 'credit_card') and any_write(env, 23) and state_has(env, 23, [['invoice'], ['budget'], ['remaining'], ['authorization']])

def s23_company_card_statement_refresh(env) -> bool:
    return stage23_finance_refresh(env)

def s23_invoice_archive_propagated(env) -> bool:
    return stage23_finance_refresh(env) and (
        used(env, 23, 'notion')
        or used(env, 23, 'email', 'save_draft')
        or used(env, 23, 'notification_hub')
    )

CHECKS = [
    ('s23_invoice_budget_reconcile', s23_invoice_budget_reconcile, 1.5),
    ('s23_company_card_statement_refresh', s23_company_card_statement_refresh, 1.0),
    ('s23_invoice_archive_propagated', s23_invoice_archive_propagated, 1.0),
]
