from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['banking', 'email', 'legal_search', 'calendar']
TERMS = ['12000000', 'mandatory', 'defer', '800000']

def s7_prioritization_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 7, SERVERS, TERMS, min_servers=3, min_terms=2)

def s7_prioritization_durable_state(env) -> bool:
    return stage_durable_evidence(env, 7, TERMS, min_terms=2, min_files=2)

def s7_prioritization_authorization_state(env) -> bool:
    return stage_authority_gate(env, 7, TERMS)

CHECKS = [
    ('s7_prioritization_source_chain', s7_prioritization_source_chain, 0.35),
    ('s7_prioritization_durable_state', s7_prioritization_durable_state, 0.40),
    ('s7_prioritization_authorization_state', s7_prioritization_authorization_state, 0.35),
]
