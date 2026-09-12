from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['email', 'notification_hub', 'legal_search']
TERMS = ['em-air-pass-0718', 'ntf_air_pass_0718', 'AQ-2026-0718-HJ603', '0.055']

def s17_official_air_result_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 17, SERVERS, TERMS, min_servers=3, min_terms=2)

def s17_official_air_result_durable_state(env) -> bool:
    return stage_durable_evidence(env, 17, TERMS, min_terms=2, min_files=2)

def s17_official_air_result_authorization_state(env) -> bool:
    return stage_authority_gate(env, 17, TERMS)

def s17_air_result_paid_and_verified(env) -> bool:
    return (
        official_air_test_payment_trace(env)
        and air_test_paid(env)
        and air_quality_passed(env)
        and notification_rechecked_after(env, AIR_PASS_NOTIFICATION, 17)
        and source_matrix_complete(env, TERMS + [str(AIR_TEST_MINOR)], threshold=4)
    )

CHECKS = [
    ('s17_official_air_result_source_chain', s17_official_air_result_source_chain, 0.35),
    ('s17_official_air_result_durable_state', s17_official_air_result_durable_state, 0.40),
    ('s17_official_air_result_authorization_state', s17_official_air_result_authorization_state, 0.35),
    ('s17_air_result_paid_and_verified', s17_air_result_paid_and_verified, 1.75),
]
