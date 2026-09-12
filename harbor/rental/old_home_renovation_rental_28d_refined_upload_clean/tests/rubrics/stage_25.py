from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['banking', 'listing_platform', 'calendar', 'ecommerce', 'delivery_logistics']
TERMS = ['AQ-2026-0718-HJ603', 'AC-2026-0716-HJ603', 'prod_haier_fridge_210l', '2026-07-28']

def s25_final_handoff_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 25, SERVERS, TERMS, min_servers=3, min_terms=3)

def s25_final_handoff_durable_state(env) -> bool:
    return stage_durable_evidence(env, 25, TERMS, min_terms=3, min_files=2)

def s25_final_handoff_authorization_state(env) -> bool:
    return stage_authority_gate(env, 25, TERMS)

def s25_final_backend_summary_consistent(env) -> bool:
    text = workspace_file(env, 'final_summary.md') + '\n' + workspace_file(env, 'rental_timeline.md')
    return (
        s25_final_handoff_authorization_state(env)
        and rental_listing_exact_backend(env)
        and viewing_scheduled_after_ready(env)
        and handover_calendar_after_ready(env)
        and count_any(text, [AIR_REPORT_NO, ACCEPTANCE_NO, READY_DATE, OFFICIAL_CONTRACTOR_PAYEE, 'prod_haier_fridge_210l']) >= 5
    )

CHECKS = [
    ('s25_final_handoff_source_chain', s25_final_handoff_source_chain, 0.35),
    ('s25_final_handoff_durable_state', s25_final_handoff_durable_state, 0.40),
    ('s25_final_handoff_authorization_state', s25_final_handoff_authorization_state, 0.35),
    ('s25_final_backend_summary_consistent', s25_final_backend_summary_consistent, 1.75),
]
