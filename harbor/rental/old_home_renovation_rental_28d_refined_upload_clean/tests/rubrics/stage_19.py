from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['delivery_logistics', 'calendar', 'notification_hub']
TERMS = ['ship_fridge_0721', 'ship_washer_0721', '2026-07-21', 'elevator']

def s19_delivery_window_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 19, SERVERS, TERMS, min_servers=3, min_terms=2)

def s19_delivery_window_durable_state(env) -> bool:
    return stage_durable_evidence(env, 19, TERMS, min_terms=2, min_files=2)

def s19_delivery_window_authorization_state(env) -> bool:
    return stage_authority_gate(env, 19, TERMS)

def s19_delivery_subscription_and_window(env) -> bool:
    return (
        exact_valid_appliance_order(env)
        and delivery_checked(env)
        and delivery_subscription_active(env)
        and delivery_window_recorded(env)
    )

CHECKS = [
    ('s19_delivery_window_source_chain', s19_delivery_window_source_chain, 0.35),
    ('s19_delivery_window_durable_state', s19_delivery_window_durable_state, 0.40),
    ('s19_delivery_window_authorization_state', s19_delivery_window_authorization_state, 0.35),
    ('s19_delivery_subscription_and_window', s19_delivery_subscription_and_window, 1.75),
]
