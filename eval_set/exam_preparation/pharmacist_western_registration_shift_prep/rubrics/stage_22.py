from __future__ import annotations

from ._helpers import course_order_complete, persistent_record, stage_calendar_event_written, successful_result_contains


def r38_law_patch_detected(env) -> bool:
    return bool(
        course_order_complete(env)
        and (
            successful_result_contains(env, "ecommerce", None, 22, "prod_law_patch_2026")
            or successful_result_contains(env, "ecommerce", None, 22, "sku_law_patch_2026")
        )
    )


def r39_patch_study_scheduled(env) -> bool:
    return bool(
        r38_law_patch_detected(env)
        and (
            stage_calendar_event_written(env, 22, "法规")
            or persistent_record(env, 22, "sku_law_patch_2026", "法规补丁", min_hits=1)
        )
    )


CHECKS = [
    ("r38_law_patch_detected", r38_law_patch_detected, 1.5),
    ("r39_patch_study_scheduled", r39_patch_study_scheduled, 1.5),
]
