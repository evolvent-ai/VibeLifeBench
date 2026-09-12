from __future__ import annotations
from ._helpers import *

def s2_scheduled_monitor_setup(env) -> bool:
    return bool(
        tool_stage(env, 2, 'notification_hub', None)
        and tool_stage(env, 2, 'calendar', None)
        and subscription_has_parts(env, ('listing_platform', 'active'))
        and calendar_has_event_parts(env, ('rental housing', 'review'), '2026-07-14T00:00:00+08:00', '2026-08-17T00:00:00+08:00')
    )

def s2_tracker_persisted(env) -> bool:
    return bool(
        saved_has(env, C.LIST_A)
        and saved_has(env, C.LIST_C)
        and derived_stage_has(env, 2, ('last_verified_at', 'next_check_at'), ('CANDIDATE_TRACKER.md', 'HEARTBEAT.md'))
    )

CHECKS = [
    ("s2_scheduled_monitor_setup", s2_scheduled_monitor_setup, 1.25),
    ("s2_tracker_persisted", s2_tracker_persisted, 1.25),
]
