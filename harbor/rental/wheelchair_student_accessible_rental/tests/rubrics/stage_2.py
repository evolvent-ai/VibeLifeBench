from __future__ import annotations
from ._helpers import *


def s2_scheduled_monitor_setup(env) -> bool:
    core_review = stage_calendar_persisted(
        env,
        2,
        [
            ("rental", "candidate"),
            ("recheck",),
            ("status", "listing status", "status"),
            ("price", "price", "price_minor"),
            ("route", "campus entrance", "entrance"),
        ],
    )
    family_time_review = stage_calendar_persisted(
        env,
        2,
        [
            ("rental", "candidate"),
            ("recheck",),
            ("family", "family viewing"),
            ("time", "conflict", "8/8", "8/9"),
        ],
    )
    cadence_record = stage_record_persisted(
        env,
        2,
        [
            ("recheck", "reminder"),
            ("status", "listing status", "status"),
            ("price", "price", "price_minor"),
            ("route", "campus entrance", "entrance"),
            ("family", "family viewing"),
            ("time", "conflict", "8/8", "8/9"),
        ],
        files=("HEARTBEAT.md", "REVIEW_CADENCE.md"),
    )
    return core_review and family_time_review and cadence_record


def s2_tracker_persisted(env) -> bool:
    return (
        s2_scheduled_monitor_setup(env)
        and stage_record_persisted(
            env,
            2,
            [
                ("candidate", "listing"),
                ("price", "price", "price_minor"),
                ("route", "campus entrance", "entrance"),
                ("family", "family viewing", "only viewing weekend"),
                ("authorization", "pending confirmation"),
            ],
            files=("CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
    )


CHECKS = [
    ('s2_scheduled_monitor_setup', s2_scheduled_monitor_setup, 1.25),
    ('s2_tracker_persisted', s2_tracker_persisted, 1.25),
]
