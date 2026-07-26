from __future__ import annotations
from ._helpers import *


def s2_scheduled_monitor_setup(env) -> bool:
    core_review = stage_calendar_persisted(
        env,
        2,
        [
            ("租房", "候选"),
            ("复核",),
            ("状态", "房态", "status"),
            ("价格",),
        ],
    )
    route_and_weekend_review = stage_calendar_persisted(
        env,
        2,
        [
            ("复核",),
            ("路线", "通勤"),
            ("唯一看房周末", "唯一线下看房周末", "看房周末"),
        ],
    )
    return (
        core_review
        and route_and_weekend_review
        and stage_record_persisted(
            env,
            2,
            [
                ("复核", "提醒"),
                ("状态", "房态", "status"),
                ("价格", "price", "price_minor"),
                ("路线", "通勤"),
                ("邮件",),
                ("唯一看房周末",),
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
            [("候选", "房源"), ("价格",), ("路线",), ("授权", "待确认")],
            files=("CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
    )


CHECKS = [
    ("s2_scheduled_monitor_setup", s2_scheduled_monitor_setup, 1.25),
    ("s2_tracker_persisted", s2_tracker_persisted, 1.25),
]
