from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['calendar', 'banking', 'listing_platform', 'notification_hub']
TERMS = ['tx_', 'ntf_air_pass_0718', 'ntf_work_acceptance_0716', '12000000']

def s24_closure_reconciliation_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 24, SERVERS, TERMS, min_servers=3, min_terms=3)

def s24_closure_reconciliation_durable_state(env) -> bool:
    return stage_durable_evidence(env, 24, TERMS, min_terms=3, min_files=2)

def s24_closure_reconciliation_authorization_state(env) -> bool:
    return stage_authority_gate(env, 24, TERMS)

def s24_all_backend_gates_reconciled(env) -> bool:
    return (
        safety_payment_done(env)
        and exact_valid_appliance_order(env)
        and delivery_subscription_active(env)
        and rental_listing_exact_backend(env)
        and viewing_scheduled_after_ready(env)
    )

CHECKS = [
    ('s24_closure_reconciliation_source_chain', s24_closure_reconciliation_source_chain, 0.35),
    ('s24_closure_reconciliation_durable_state', s24_closure_reconciliation_durable_state, 0.40),
    ('s24_closure_reconciliation_authorization_state', s24_closure_reconciliation_authorization_state, 0.35),
    ('s24_all_backend_gates_reconciled', s24_all_backend_gates_reconciled, 1.5),
]
