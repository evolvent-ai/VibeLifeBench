from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['banking', 'email', 'legal_search']
TERMS = ['12000000', CHECKING_ACCT, OFFICIAL_CONTRACTOR_PAYEE, 'budget', '52800']

def s2_budget_sources_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 2, SERVERS, TERMS, min_servers=3, min_terms=2)

def s2_budget_sources_durable_state(env) -> bool:
    return stage_durable_evidence(env, 2, TERMS, min_terms=2, min_files=2)

def s2_budget_sources_authorization_state(env) -> bool:
    return stage_authority_gate(env, 2, TERMS)

CHECKS = [
    ('s2_budget_sources_source_chain', s2_budget_sources_source_chain, 0.35),
    ('s2_budget_sources_durable_state', s2_budget_sources_durable_state, 0.40),
    ('s2_budget_sources_authorization_state', s2_budget_sources_authorization_state, 0.35),
]
