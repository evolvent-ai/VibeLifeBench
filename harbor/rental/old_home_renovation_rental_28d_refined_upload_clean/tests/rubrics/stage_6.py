from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['notification_hub', 'calendar', 'email']
TERMS = ['ntf_property_complaint_0706', 'quiet_hours', '12:00-14:00', '18:00']

def s6_quiet_hours_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 6, SERVERS, TERMS, min_servers=3, min_terms=2)

def s6_quiet_hours_durable_state(env) -> bool:
    return stage_durable_evidence(env, 6, TERMS, min_terms=2, min_files=2)

def s6_quiet_hours_authorization_state(env) -> bool:
    return stage_authority_gate(env, 6, TERMS)

CHECKS = [
    ('s6_quiet_hours_source_chain', s6_quiet_hours_source_chain, 0.35),
    ('s6_quiet_hours_durable_state', s6_quiet_hours_durable_state, 0.40),
    ('s6_quiet_hours_authorization_state', s6_quiet_hours_authorization_state, 0.35),
]
