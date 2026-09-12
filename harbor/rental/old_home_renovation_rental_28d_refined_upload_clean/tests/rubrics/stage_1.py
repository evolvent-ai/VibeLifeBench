from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['notification_hub', 'email', 'calendar']
TERMS = ['ntf_property_rules_0702', 'quiet_hours', 'cal_zl_rental_reno', 'property_constraints']

def s1_property_rules_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 1, SERVERS, TERMS, min_servers=3, min_terms=2)

def s1_property_rules_durable_state(env) -> bool:
    return stage_durable_evidence(env, 1, TERMS, min_terms=2, min_files=2)

def s1_property_rules_authorization_state(env) -> bool:
    return stage_authority_gate(env, 1, TERMS)

CHECKS = [
    ('s1_property_rules_source_chain', s1_property_rules_source_chain, 0.35),
    ('s1_property_rules_durable_state', s1_property_rules_durable_state, 0.40),
    ('s1_property_rules_authorization_state', s1_property_rules_authorization_state, 0.35),
]
