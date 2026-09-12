from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['ecommerce', 'banking', 'notification_hub']
TERMS = ['sku_luxe_fridge_620l_silver', 'prod_haier_fridge_210l', 'quantity', 'budget']

def s13_appliance_stock_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 13, SERVERS, TERMS, min_servers=3, min_terms=2)

def s13_appliance_stock_durable_state(env) -> bool:
    return stage_durable_evidence(env, 13, TERMS, min_terms=2, min_files=2)

def s13_appliance_stock_authorization_state(env) -> bool:
    return stage_authority_gate(env, 13, TERMS)

CHECKS = [
    ('s13_appliance_stock_source_chain', s13_appliance_stock_source_chain, 0.35),
    ('s13_appliance_stock_durable_state', s13_appliance_stock_durable_state, 0.40),
    ('s13_appliance_stock_authorization_state', s13_appliance_stock_authorization_state, 0.35),
]
