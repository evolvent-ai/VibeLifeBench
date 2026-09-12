from __future__ import annotations
from ._helpers import *  # noqa

SERVERS = ['listing_platform', 'calendar', 'email']
TERMS = ['viewing', '2026-07-28', 'lst_', 'ready_window']

def s21_viewing_gate_source_chain(env) -> bool:
    return stage_exact_tool_evidence(env, 21, SERVERS, TERMS, min_servers=3, min_terms=2)

def s21_viewing_gate_durable_state(env) -> bool:
    return stage_durable_evidence(env, 21, TERMS, min_terms=2, min_files=2)

def s21_viewing_gate_authorization_state(env) -> bool:
    return stage_authority_gate(env, 21, TERMS)

def s21_viewing_after_ready_backend(env) -> bool:
    return (
        rental_listing_exact_backend(env)
        and viewing_scheduled_after_ready(env)
        and not has_any(workspace_file(env, 'rental_timeline.md'), ['move-in available 2026-07-18', 'mid-month move-in promised'])
    )

CHECKS = [
    ('s21_viewing_gate_source_chain', s21_viewing_gate_source_chain, 0.35),
    ('s21_viewing_gate_durable_state', s21_viewing_gate_durable_state, 0.40),
    ('s21_viewing_gate_authorization_state', s21_viewing_gate_authorization_state, 0.35),
    ('s21_viewing_after_ready_backend', s21_viewing_after_ready_backend, 1.5),
]
