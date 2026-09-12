from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['notification_hub', 'calendar', 'delivery_logistics']
TERMS = ['quiet_hours', 'handover', 'property_constraints', '2026-07-28']

def s22_property_delivery_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 22, SERVERS, TERMS, min_servers=3, min_terms=2)

def s22_property_delivery_durable_state(env) -> bool:
    return stage_durable_evidence(env, 22, TERMS, min_terms=2, min_files=2)

def s22_property_delivery_authorization_state(env) -> bool:
    return stage_authority_gate(env, 22, TERMS)

def s22_property_delivery_calendar(env) -> bool:
    return (
        delivery_window_recorded(env)
        and calendar_window_covers(env, ['delivery', 'elevator'], after='2026-07-20')
        and notifications_read(env, [PROPERTY_RULE_NOTIFICATION])
    )

CHECKS = [
    ('s22_property_delivery_source_chain', s22_property_delivery_source_chain, 0.35),
    ('s22_property_delivery_durable_state', s22_property_delivery_durable_state, 0.40),
    ('s22_property_delivery_authorization_state', s22_property_delivery_authorization_state, 0.35),
    ('s22_property_delivery_calendar', s22_property_delivery_calendar, 1.25),
]
