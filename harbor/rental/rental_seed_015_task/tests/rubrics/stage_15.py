from __future__ import annotations
from ._helpers import *


def s15_school_schedule_recovery(env) -> bool:
    return (
        stage_ok(env, 15, "s15")
        and _has_parts(calendar_event("evt_school_early_release", env), ["16:35", "17:20"])
        and listing_d_backup_backend_ready(env)
        and notion_has_any(env, (["early dismissal", "evening route", "17:20"], ["office-to-school", "pick up child", "care"]))
    )


def s15_care_matrix_created(env) -> bool:
    return stage_ok(env, 15, "s15") and care_matrix_backend_ready(env)


CHECKS = [
    ("s15_school_schedule_recovery", s15_school_schedule_recovery, 1.75),
    ("s15_care_matrix_created", s15_care_matrix_created, 1.5),
]
