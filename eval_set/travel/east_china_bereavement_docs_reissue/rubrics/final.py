from __future__ import annotations

from ._helpers import (
    check_final_all_segments_closed,
    check_final_archive_consistent,
    check_final_budget_reasoned_summary,
    check_final_sensitive_boundary_preserved,
)


def final_all_segments_closed(env) -> bool:
    return check_final_all_segments_closed(env)


def final_sensitive_boundary_preserved(env) -> bool:
    return check_final_sensitive_boundary_preserved(env)


def final_budget_reasoned_summary(env) -> bool:
    return check_final_budget_reasoned_summary(env)


def final_archive_consistent(env) -> bool:
    return check_final_archive_consistent(env)


CHECKS = [
    ("final_all_segments_closed", final_all_segments_closed, 3.0),
    ("final_sensitive_boundary_preserved", final_sensitive_boundary_preserved, 3.0),
    ("final_budget_reasoned_summary", final_budget_reasoned_summary, 3.0),
    ("final_archive_consistent", final_archive_consistent, 3.0),
]
