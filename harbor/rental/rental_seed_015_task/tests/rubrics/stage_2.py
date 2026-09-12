from __future__ import annotations
from ._helpers import *


def s2_calendar_baseline(env) -> bool:
    return (
        stage_ok(env, 2, "s2")
        and calendar_baseline_backend_ready(env)
        and notion_has_any(env, (["work hours", "aftercare", "parent meeting", "lease expiration"], ["09:30", "17:30", "18:00", "2026-08-08"]))
    )


def s2_recurring_review_setup(env) -> bool:
    return (
        stage_ok(env, 2, "s2")
        and recurring_review_backend_ready(env)
        and notion_has_any(env, (["72", "review", "listing", "route"], ["three days", "elevator", "calendar"]))
    )


CHECKS = [
    ("s2_calendar_baseline", s2_calendar_baseline, 1.25),
    ("s2_recurring_review_setup", s2_recurring_review_setup, 1.25),
]
