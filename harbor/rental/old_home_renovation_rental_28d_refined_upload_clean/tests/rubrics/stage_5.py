from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['email', 'legal_search', 'banking']
TERMS = ['em-electrical-aging-0705', '29200', '110600', 'circuit_aging', 'leakage_protector']

def s5_electrical_assessment_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 5, SERVERS, TERMS, min_servers=3, min_terms=2)

def s5_electrical_assessment_durable_state(env) -> bool:
    return stage_durable_evidence(env, 5, TERMS, min_terms=2, min_files=2)

def s5_electrical_assessment_authorization_state(env) -> bool:
    return stage_authority_gate(env, 5, TERMS)

CHECKS = [
    ('s5_electrical_assessment_source_chain', s5_electrical_assessment_source_chain, 0.35),
    ('s5_electrical_assessment_durable_state', s5_electrical_assessment_durable_state, 0.40),
    ('s5_electrical_assessment_authorization_state', s5_electrical_assessment_authorization_state, 0.35),
]
