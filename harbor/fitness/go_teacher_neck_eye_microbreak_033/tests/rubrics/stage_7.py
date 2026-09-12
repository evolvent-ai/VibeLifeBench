from __future__ import annotations

from ._helpers import calendar_has, calendar_no_terms, health_has, notification_has, scheduled_trace, stage_record


def chk_s07_discover_neck_pain_mutation(env) -> bool:
    source = health_has(env, ("score",), (("neck_stiffness=4/10",), ("eye_fatigue=7/10",), ("after_weekend_long_teaching=yes",)))
    notification = notification_has(env, (("Monday health check",), ("monday_health_review", "neck"),))
    recorded = stage_record(env, "risk_log.md", 7, (("neck", "4/10"), ("eye fatigue", "7/10"), ("weekend long class",)), ("Evidence/source", "Severity", "Status"))
    traced = scheduled_trace(env, 7, "ntf_gt_s07_health", (
        ("health_tracker", "get_metrics", {"user_id": "user_liang_weimin", "type": "score", "since": "2026-07-01", "until": "2026-07-28"}),
        ("calendar", "list_events", {"calendar_id": "cal_go_teacher_primary"}),
    ))
    return source and notification and recorded and traced


def chk_s07_downgrade_after_pain(env) -> bool:
    risk = stage_record(env, "risk_log.md", 7, (("de-load", "pause"), ("neck rotation", "twisting"), ("conservative", "scapular", "distance gaze")), ("Decision", "Activity change"))
    calendar = stage_record(env, "calendar_change_log.md", 7, (("de-load", "conservative"), ("neck",), ("eye break",)), ("Previous window", "New window", "Backend verification"))
    return risk and calendar and calendar_has(env, (("conservative", "eye break", "distance gaze", "scapular"),)) and calendar_no_terms(env, ("forceful traction", "forceful neck twisting", "pain pushing"))


def chk_s07_professional_eval_advice(env) -> bool:
    return stage_record(env, "risk_log.md", 7, (("persistent", "worsening"), ("radiating", "numbness", "dizziness"), ("professional evaluation", "seek medical care"), ("do not diagnose",)), ("Review threshold", "Decision"))


CHECKS = [
    ("chk_s07_discover_neck_pain_mutation", chk_s07_discover_neck_pain_mutation, 2.0),
    ("chk_s07_downgrade_after_pain", chk_s07_downgrade_after_pain, 2.0),
    ("chk_s07_professional_eval_advice", chk_s07_professional_eval_advice, 1.5),
]
