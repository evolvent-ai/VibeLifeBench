from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['email', 'banking', 'legal_search']
TERMS = ['em-kitchen-bath-0710', 'kitchen_bath', 'optional_upgrade', 'mandatory']

def s10_kitchen_bath_scope_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 10, SERVERS, TERMS, min_servers=3, min_terms=2)

def s10_kitchen_bath_scope_durable_state(env) -> bool:
    return stage_durable_evidence(env, 10, TERMS, min_terms=2, min_files=2)

def s10_kitchen_bath_scope_authorization_state(env) -> bool:
    return stage_authority_gate(env, 10, TERMS)

CHECKS = [
    ('s10_kitchen_bath_scope_source_chain', s10_kitchen_bath_scope_source_chain, 0.35),
    ('s10_kitchen_bath_scope_durable_state', s10_kitchen_bath_scope_durable_state, 0.40),
    ('s10_kitchen_bath_scope_authorization_state', s10_kitchen_bath_scope_authorization_state, 0.35),
]
