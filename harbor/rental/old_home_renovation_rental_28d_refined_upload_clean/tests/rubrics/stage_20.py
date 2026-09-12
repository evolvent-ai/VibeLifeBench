from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['listing_platform', 'legal_search', 'calendar']
TERMS = ['lst_rental_profile_hj603', 'AQ-2026-0718-HJ603', 'AC-2026-0716-HJ603', 'rent']

def s20_listing_gate_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 20, SERVERS, TERMS, min_servers=3, min_terms=2)

def s20_listing_gate_durable_state(env) -> bool:
    return stage_durable_evidence(env, 20, TERMS, min_terms=2, min_files=2)

def s20_listing_gate_authorization_state(env) -> bool:
    return stage_authority_gate(env, 20, TERMS)

def s20_listing_posted_with_gates(env) -> bool:
    return (
        rental_listing_exact_backend(env)
        and work_acceptance_verified(env)
        and air_quality_passed(env)
        and no_early_listing_commitment(env)
    )

CHECKS = [
    ('s20_listing_gate_source_chain', s20_listing_gate_source_chain, 0.35),
    ('s20_listing_gate_durable_state', s20_listing_gate_durable_state, 0.40),
    ('s20_listing_gate_authorization_state', s20_listing_gate_authorization_state, 0.35),
    ('s20_listing_posted_with_gates', s20_listing_posted_with_gates, 2.0),
]
