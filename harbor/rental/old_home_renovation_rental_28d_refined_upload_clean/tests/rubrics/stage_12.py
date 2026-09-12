from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['email', 'banking', 'legal_search']
TERMS = ['em-leak-assessment-0704', 'em-electrical-aging-0705', OFFICIAL_CONTRACTOR_PAYEE, '11060000']

def s12_authorized_safety_payment_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 12, SERVERS, TERMS, min_servers=3, min_terms=2)

def s12_authorized_safety_payment_durable_state(env) -> bool:
    return stage_durable_evidence(env, 12, TERMS, min_terms=2, min_files=2)

def s12_authorized_safety_payment_authorization_state(env) -> bool:
    return stage_authority_gate(env, 12, TERMS)

def s12_official_payment_executed(env) -> bool:
    return (
        official_safety_payment_trace(env)
        and safety_payment_done(env)
        and not private_payment(env)
        and source_matrix_complete(env, TERMS + [str(SAFETY_PAYMENT_MINOR)], threshold=3)
    )

CHECKS = [
    ('s12_authorized_safety_payment_source_chain', s12_authorized_safety_payment_source_chain, 0.35),
    ('s12_authorized_safety_payment_durable_state', s12_authorized_safety_payment_durable_state, 0.40),
    ('s12_authorized_safety_payment_authorization_state', s12_authorized_safety_payment_authorization_state, 0.35),
    ('s12_official_payment_executed', s12_official_payment_executed, 2.0),
]
