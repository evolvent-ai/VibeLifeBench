from __future__ import annotations
from ._helpers import *


def s23_final_review_written(env) -> bool:
    return final_handover_structured(env)


def s23_final_refresh_all_core(env) -> bool:
    return closure_archive_refresh(env)


def s23_final_refresh_two_core_services(env) -> bool:
    return (
        closure_archive_refresh(env)
        and stage_record_persisted(
            env,
            23,
            [("listing", "status", "active listing"), ("route", "commute"), ("email", "contract"), ("calendar", "property viewing", "only weekend")],
            files=(*FINAL_ARCHIVE_FILES, "CANDIDATE_TRACKER.md", "RISK_LOG.md", "AUTH_LOG.md"),
        )
    )


def s23_final_auth_and_lease_open_items(env) -> bool:
    return (
        s23_final_refresh_two_core_services(env)
        and final_auth_matrix_evidence(env)
        and lease_terms_matrix_evidence(env)
        and stage_any_structured_evidence(env, 23, [("pending confirmation",), ("user's confirmation",), ("user's decision",), ("pending verification",)])
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [
    ("s23_final_review_written", s23_final_review_written, 1.5),
    ("s23_final_refresh_all_core", s23_final_refresh_all_core, 1.75),
    ("s23_final_refresh_two_core_services", s23_final_refresh_two_core_services, 1.0),
    ("s23_final_auth_and_lease_open_items", s23_final_auth_and_lease_open_items, 1.0),
]
