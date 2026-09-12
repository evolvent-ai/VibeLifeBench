from __future__ import annotations

from ._helpers import no_forbidden_orders, paid_order_count, successful_result_contains


def r10_course_candidates_official(env) -> bool:
    return bool(
        successful_result_contains(env, "ecommerce", None, 5, "prod_west_p1_2026")
        and successful_result_contains(env, "ecommerce", None, 5, "prod_law_2026")
        and successful_result_contains(env, "ecommerce", None, 5, "western_pharmacist")
    )


def r11_gray_sku_excluded_initial(env) -> bool:
    bad_checked = bool(
        successful_result_contains(env, "ecommerce", None, 5, "prod_broker_pass")
        or successful_result_contains(env, "ecommerce", None, 5, "prod_chinese_bundle")
    )
    return bool(
        r10_course_candidates_official(env)
        and bad_checked
        and paid_order_count(env) == 0
        and no_forbidden_orders(env)
    )


CHECKS = [
    ("r10_course_candidates_official", r10_course_candidates_official, 1.5),
    ("r11_gray_sku_excluded_initial", r11_gray_sku_excluded_initial, 1.5),
]
