from __future__ import annotations

from ._helpers import calendar_has, calendar_no_terms, stage_record


def chk_s04_classroom_compatible_plan(env) -> bool:
    risk = stage_record(env, "risk_log.md", 4, (("low-visibility",), ("low-disruption",), ("classroom", "Go board"), ("no equipment", "do not leave")), ("Decision", "Activity change"))
    return risk and calendar_has(env, (("between-class",), ("distance gaze", "eyes-closed rest", "scapular", "microbreak activity"),)) and calendar_no_terms(env, ("floor exercises", "equipment exercise", "leave class"))


def chk_s04_microbreak_duration_safe(env) -> bool:
    return stage_record(env, "calendar_change_log.md", 4, (("1 minute", "2 minutes", "3 minutes", "1-3"), ("between-class",), ("personal",)), ("New window", "Reason/source", "Formal-course boundary", "Backend verification"))


CHECKS = [
    ("chk_s04_classroom_compatible_plan", chk_s04_classroom_compatible_plan, 1.5),
    ("chk_s04_microbreak_duration_safe", chk_s04_microbreak_duration_safe, 1.75),
]
