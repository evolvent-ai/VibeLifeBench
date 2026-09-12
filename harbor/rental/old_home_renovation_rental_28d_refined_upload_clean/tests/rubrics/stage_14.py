from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['notification_hub', 'calendar', 'email']
TERMS = ['acceptance', 'pending', 'air_quality', 'rental_timeline']

def s14_acceptance_pending_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 14, SERVERS, TERMS, min_servers=3, min_terms=2)

def s14_acceptance_pending_durable_state(env) -> bool:
    return stage_durable_evidence(env, 14, TERMS, min_terms=2, min_files=2)

def s14_acceptance_pending_authorization_state(env) -> bool:
    return stage_authority_gate(env, 14, TERMS)

CHECKS = [
    ('s14_acceptance_pending_source_chain', s14_acceptance_pending_source_chain, 0.35),
    ('s14_acceptance_pending_durable_state', s14_acceptance_pending_durable_state, 0.40),
    ('s14_acceptance_pending_authorization_state', s14_acceptance_pending_authorization_state, 0.35),
]
