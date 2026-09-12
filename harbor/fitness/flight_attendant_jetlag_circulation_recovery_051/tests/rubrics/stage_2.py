from __future__ import annotations

from ._helpers import calendar_has, stage_record


def chk_s02_scheduled_checks(env) -> bool:
    scheduled = calendar_has(env, (("health", "recovery"), ("weather",), ("order", "equipment"), ("private status", "recovery status"), ("review",)))
    logged = stage_record(
        env,
        "calendar_change_log.md",
        2,
        (("health", "recovery"), ("weather",), ("order", "equipment"), ("cycle",), ("private status", "recovery status"), ("review",)),
        ("Calendar object", "New window", "Reason/source", "Backend verification"),
    )
    return scheduled and logged


CHECKS = [("chk_s02_scheduled_checks", chk_s02_scheduled_checks, 1.5)]
