from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['notification_hub', 'email', 'calendar']
TERMS = ['ntf_work_acceptance_0716', 'AC-2026-0716-HJ603', 'mandatory_done', 'air']

def s15_acceptance_verified_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 15, SERVERS, TERMS, min_servers=3, min_terms=2)

def s15_acceptance_verified_durable_state(env) -> bool:
    return stage_durable_evidence(env, 15, TERMS, min_terms=2, min_files=2)

def s15_acceptance_verified_authorization_state(env) -> bool:
    return stage_authority_gate(env, 15, TERMS)

def s15_acceptance_after_payment(env) -> bool:
    return (
        official_safety_payment_trace(env)
        and work_acceptance_verified(env)
        and notification_rechecked_after(env, ACCEPTANCE_NOTIFICATION, 15)
    )

CHECKS = [
    ('s15_acceptance_verified_source_chain', s15_acceptance_verified_source_chain, 0.35),
    ('s15_acceptance_verified_durable_state', s15_acceptance_verified_durable_state, 0.40),
    ('s15_acceptance_verified_authorization_state', s15_acceptance_verified_authorization_state, 0.35),
    ('s15_acceptance_after_payment', s15_acceptance_after_payment, 1.5),
]
