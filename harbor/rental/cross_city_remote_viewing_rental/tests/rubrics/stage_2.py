from __future__ import annotations
from ._helpers import *


def s2_scheduled_monitor_setup(env) -> bool:
    core_review = stage_calendar_persisted(
        env,
        2,
        [
            ("rental", "candidate"),
            ("review",),
            ("status", "listing status", "status"),
            ("price",),
        ],
    )
    route_and_weekend_review = stage_calendar_persisted(
        env,
        2,
        [
            ("review",),
            ("route", "commute"),
            ("only in-person viewing weekend", "only in-person viewing weekend", "viewing weekend"),
        ],
    )
    return (
        core_review
        and route_and_weekend_review
        and stage_record_persisted(
            env,
            2,
            [
                ("review", "reminder"),
                ("status", "listing status", "status"),
                ("price", "price", "price_minor"),
                ("route", "commute"),
                ("email",),
                ("only in-person viewing weekend",),
            ],
            files=("HEARTBEAT.md", "REVIEW_CADENCE.md", "REVIEW_RHYTHM.md"),
        )
    )


def s2_tracker_persisted(env) -> bool:
    return (
        s2_scheduled_monitor_setup(env)
        and stage_record_persisted(
            env,
            2,
            [("candidate", "listing"), ("price",), ("route",), ("authorization", "pending confirmation")],
            files=("CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
    )


CHECKS = [
    ("s2_scheduled_monitor_setup", s2_scheduled_monitor_setup, 1.25),
    ("s2_tracker_persisted", s2_tracker_persisted, 1.25),
]
