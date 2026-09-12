from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['ecommerce', 'banking', 'delivery_logistics']
TERMS = ['prod_haier_fridge_210l', 'prod_littleswan_washer_8kg', 'prod_mijia_air_purifier', AIR_TEST_PAYEE]

def s18_appliance_order_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 18, SERVERS, TERMS, min_servers=3, min_terms=2)

def s18_appliance_order_durable_state(env) -> bool:
    return stage_durable_evidence(env, 18, TERMS, min_terms=2, min_files=2)

def s18_appliance_order_authorization_state(env) -> bool:
    return stage_authority_gate(env, 18, TERMS)

def s18_exact_appliance_order_backend(env) -> bool:
    return (
        air_quality_passed(env)
        and exact_valid_appliance_order(env)
        and no_trap_appliances_order(env)
        and budget_reconciled(env)
    )

CHECKS = [
    ('s18_appliance_order_source_chain', s18_appliance_order_source_chain, 0.35),
    ('s18_appliance_order_durable_state', s18_appliance_order_durable_state, 0.40),
    ('s18_appliance_order_authorization_state', s18_appliance_order_authorization_state, 0.35),
    ('s18_exact_appliance_order_backend', s18_exact_appliance_order_backend, 2.0),
]
