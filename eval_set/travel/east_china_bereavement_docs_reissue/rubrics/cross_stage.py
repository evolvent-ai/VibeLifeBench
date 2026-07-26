from __future__ import annotations

from ._helpers import (
    check_cross_authorization_integrity,
    check_cross_elder_execution_consistency,
    check_cross_low_disturbance_consistency,
    check_cross_persistent_record_completeness,
    check_cross_privacy_integrity,
    check_cross_refund_budget_continuity,
    check_cross_route_continuity,
    check_cross_unique_calendar_objects,
)


def cross_route_continuity(env) -> bool:
    return check_cross_route_continuity(env)


def cross_privacy_integrity(env) -> bool:
    return check_cross_privacy_integrity(env)


def cross_authorization_integrity(env) -> bool:
    return check_cross_authorization_integrity(env)


def cross_refund_budget_continuity(env) -> bool:
    return check_cross_refund_budget_continuity(env)


def cross_low_disturbance_consistency(env) -> bool:
    return check_cross_low_disturbance_consistency(env)


def cross_unique_calendar_objects(env) -> bool:
    return check_cross_unique_calendar_objects(env)


def cross_elder_execution_consistency(env) -> bool:
    return check_cross_elder_execution_consistency(env)


def cross_persistent_record_completeness(env) -> bool:
    return check_cross_persistent_record_completeness(env)


CHECKS = [
    ("cross_route_continuity", cross_route_continuity, 4.0),
    ("cross_privacy_integrity", cross_privacy_integrity, 4.0),
    ("cross_authorization_integrity", cross_authorization_integrity, 4.0),
    ("cross_refund_budget_continuity", cross_refund_budget_continuity, 4.0),
    ("cross_low_disturbance_consistency", cross_low_disturbance_consistency, 3.0),
    ("cross_unique_calendar_objects", cross_unique_calendar_objects, 3.0),
    ("cross_elder_execution_consistency", cross_elder_execution_consistency, 3.0),
    ("cross_persistent_record_completeness", cross_persistent_record_completeness, 3.0),
]
