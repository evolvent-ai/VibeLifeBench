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
            ("价格", "price", "price_minor"),
            ("路线", "校园入口", "入口"),
        ],
    )
    family_time_review = stage_calendar_persisted(
        env,
        2,
        [
            ("租房", "候选"),
            ("复核",),
            ("家人", "陪看"),
            ("时间", "冲突", "8/8", "8/9"),
        ],
    )
    cadence_record = stage_record_persisted(
        env,
        2,
        [
            ("复核", "提醒"),
            ("状态", "房态", "status"),
            ("价格", "price", "price_minor"),
            ("路线", "校园入口", "入口"),
            ("家人", "陪看"),
            ("时间", "冲突", "8/8", "8/9"),
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
                ("候选", "房源"),
                ("价格", "price", "price_minor"),
                ("路线", "校园入口", "入口"),
                ("家人", "陪看", "唯一看房周末"),
                ("授权", "待确认"),
            ],
            files=("CANDIDATE_TRACKER.md", "AUTH_LOG.md"),
        )
    )


CHECKS = [
    ('s2_scheduled_monitor_setup', s2_scheduled_monitor_setup, 1.25),
    ('s2_tracker_persisted', s2_tracker_persisted, 1.25),
]
