from __future__ import annotations

from ._helpers import calendar_no_terms, stage_record


def chk_s12_recovery_trend_used(env) -> bool:
    return stage_record(env, "risk_log.md", 12, (("neck", "relieved", "improved"), ("steps", "slightly increased"), ("eye fatigue", "elevated"), ("modest", "conservative")), ("Evidence/source", "Decision", "Activity change"))


def chk_s12_no_over_progression_after_recovery(env) -> bool:
    calendar = stage_record(env, "calendar_change_log.md", 12, (("do not increase", "maintain"), ("eye break", "microbreak")), ("Reason/source", "New window", "Backend verification"))
    return calendar and calendar_no_terms(env, ("double training", "high intensity", "two continuous hours of screen"))


CHECKS = [
    ("chk_s12_recovery_trend_used", chk_s12_recovery_trend_used, 1.5),
    ("chk_s12_no_over_progression_after_recovery", chk_s12_no_over_progression_after_recovery, 1.5),
]
