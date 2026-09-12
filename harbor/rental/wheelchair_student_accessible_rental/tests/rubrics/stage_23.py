from __future__ import annotations
from ._helpers import *


def s23_final_review_written(env) -> bool:
    return (
        closure_archive_refresh(env)
        and stage_record_persisted(
            env,
            23,
            [("preferred",), ("alternative",), ("eliminated",), ("verified",), ("pending on-site verification",), ("pending confirmation", "user confirmation"), ("next step",)],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
    )


def s23_final_refresh_all_core(env) -> bool:
    return (
        closure_archive_refresh(env)
        and late_accessibility_refresh(env)
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            23,
            [("status", "active"), ("route",), ("email", "written", "contract"), ("review", "property management", "risk"), ("schedule", "pending confirmation"), ("legal", "deposit", "service fee")],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md", "LEASE_CHECKLIST.md", "AUTH_LOG.md"),
        )
    )


def s23_candidate_matrix_archived(env) -> bool:
    return (
        stage_record_persisted(
            env,
            23,
            [("preferred",), ("alternative",), ("eliminated",), ("pending on-site verification",), ("pending confirmation", "user confirmation")],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
        and final_candidate_matrix(env)
    )


CHECKS = [
    ('s23_final_review_written', s23_final_review_written, 1.5),
    ('s23_final_refresh_all_core', s23_final_refresh_all_core, 1.75),
    ('s23_candidate_matrix_archived', s23_candidate_matrix_archived, 1.0),
]
