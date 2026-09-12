from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['email', 'banking', 'legal_search']
TERMS = ['em-leak-assessment-0704', '12800', 'water_leak', 'mandatory']

def s4_leak_assessment_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 4, SERVERS, TERMS, min_servers=3, min_terms=2)

def s4_leak_assessment_durable_state(env) -> bool:
    return stage_durable_evidence(env, 4, TERMS, min_terms=2, min_files=2)

def s4_leak_assessment_authorization_state(env) -> bool:
    return stage_authority_gate(env, 4, TERMS)

CHECKS = [
    ('s4_leak_assessment_source_chain', s4_leak_assessment_source_chain, 0.35),
    ('s4_leak_assessment_durable_state', s4_leak_assessment_durable_state, 0.40),
    ('s4_leak_assessment_authorization_state', s4_leak_assessment_authorization_state, 0.35),
]
