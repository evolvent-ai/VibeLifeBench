from __future__ import annotations

from ._helpers import (
    course_budget_ok,
    no_forbidden_orders,
    persistent_record,
    stage_course_order_complete,
    successful_result_contains,
)


def r20_law_old_sku_rejected(env) -> bool:
    checked_old = bool(
        successful_result_contains(env, "ecommerce", None, 12, "sku_law_old_2025")
        or successful_result_contains(env, "ecommerce", None, 12, "REG_GSP_IMPL_2016")
    )
    return bool(checked_old and no_forbidden_orders(env))


def r21_four_subjects_covered(env) -> bool:
    return stage_course_order_complete(env, 12)


def r22_course_order_authorized(env) -> bool:
    return bool(
        r21_four_subjects_covered(env)
        and persistent_record(env, 12, "授权", "四科", "西药", min_hits=2)
    )


def r23_course_budget_within_limit(env) -> bool:
    return bool(r21_four_subjects_covered(env) and course_budget_ok(env, 180000))


CHECKS = [
    ("r20_law_old_sku_rejected", r20_law_old_sku_rejected, 2.0),
    ("r21_four_subjects_covered", r21_four_subjects_covered, 2.0),
    ("r22_course_order_authorized", r22_course_order_authorized, 1.5),
    ("r23_course_budget_within_limit", r23_course_budget_within_limit, 1.0),
]
