from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['banking', 'calendar', 'notification_hub']
TERMS = ['evt_budget_review_0709', 'acct_zl_renovation', 'ntf_property_complaint_0706', 'budget']

def s9_scheduled_review_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 9, SERVERS, TERMS, min_servers=3, min_terms=2)

def s9_scheduled_review_durable_state(env) -> bool:
    return stage_durable_evidence(env, 9, TERMS, min_terms=2, min_files=2)

def s9_scheduled_review_authorization_state(env) -> bool:
    return stage_authority_gate(env, 9, TERMS)

CHECKS = [
    ('s9_scheduled_review_source_chain', s9_scheduled_review_source_chain, 0.35),
    ('s9_scheduled_review_durable_state', s9_scheduled_review_durable_state, 0.40),
    ('s9_scheduled_review_authorization_state', s9_scheduled_review_authorization_state, 0.35),
]
