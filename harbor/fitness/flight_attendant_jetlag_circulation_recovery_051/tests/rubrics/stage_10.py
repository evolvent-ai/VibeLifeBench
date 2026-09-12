from __future__ import annotations

from ._helpers import calendar_has, calendar_no_terms, health_has, stage_record


def chk_s10_sleep_edema_deload(env) -> bool:
    observed = health_has(env, ("sleep_minutes", "score"), (("sleep=4.2h",), ("calf_edema=4/5",), ("fatigue=7/10",)))
    risk = stage_record(
        env,
        "risk_log.md",
        10,
        (("4.2",), ("swelling", "4/5"), ("fatigue", "7/10"), ("48 hours", "48h"), ("deload", "recovery")),
        ("Evidence/source", "Load/change", "Status"),
    )
    calendar = stage_record(env, "calendar_change_log.md", 10, (("deload", "recovery", "rest"),), ("Previous window", "New window", "Backend verification"))
    return observed and risk and calendar and calendar_has(env, (("recovery", "rest", "deload"),)) and calendar_no_terms(env, ("HIIT", "sprints", "stair climbing"))


def chk_s10_professional_threshold(env) -> bool:
    return stage_record(
        env,
        "risk_log.md",
        10,
        (("one-sided",), ("pain",), ("chest tightness", "breathing"), ("professional assessment", "doctor"), ("do not diagnose", "risk")),
        ("Review threshold", "Decision", "Status"),
    )


CHECKS = [
    ("chk_s10_sleep_edema_deload", chk_s10_sleep_edema_deload, 2.0),
    ("chk_s10_professional_threshold", chk_s10_professional_threshold, 1.5),
]
