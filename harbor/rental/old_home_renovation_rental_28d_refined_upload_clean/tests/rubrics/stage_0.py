from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['listing_platform', 'banking', 'calendar']
TERMS = ['lst_rental_profile_hj603', 'acct_zl_renovation', 'cal_zl_rental_reno', '12000000']


def s0_baseline_inventory_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 0, SERVERS, TERMS, min_servers=3, min_terms=3)


def s0_baseline_inventory_durable_state(env) -> bool:
    return stage_durable_evidence(env, 0, TERMS, min_terms=3, min_files=2)


def s0_baseline_inventory_authorization_state(env) -> bool:
    return stage_authority_gate(env, 0, TERMS)


CHECKS = [
    ('s0_baseline_inventory_source_chain', s0_baseline_inventory_source_chain, 0.35),
    ('s0_baseline_inventory_durable_state', s0_baseline_inventory_durable_state, 0.40),
    ('s0_baseline_inventory_authorization_state', s0_baseline_inventory_authorization_state, 0.35),
]
