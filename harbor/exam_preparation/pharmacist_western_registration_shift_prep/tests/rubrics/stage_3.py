from __future__ import annotations

from ._helpers import no_hard_calendar_conflicts, persistent_record, stage_calendar_event_written


def r07_study_plan_no_conflict(env) -> bool:
    subjects = persistent_record(env, 3, "Pharmacy Professional Knowledge", "Comprehensive Pharmacy", "regulations", min_hits=2)
    calendar_plan = stage_calendar_event_written(env, 3, "study review", date="2026-08")
    return bool(subjects and calendar_plan and no_hard_calendar_conflicts(env))


CHECKS = [
    ("r07_study_plan_no_conflict", r07_study_plan_no_conflict, 1.5),
]
