from __future__ import annotations
from ._helpers import *

def s23_water_outage_calendar_updated(env) -> bool:
    return (
        stage_read_result_groups(env, 23, 'notification_hub', ('get_notification',), [('notif_outage_stage23',), ('2026-07-30', 'july 30'), ('19:00',), ('23:00',)])
        and tool_stage_any(env, 23, 'calendar', [('water outage', 'repair'), ('handover', 'photography')])
        and calendar_event_exact(env, [('water outage', 'repair'), ('handover', 'photography')], '2026-07-30T19:00', '2026-07-30T23:00')
    )

def s23_outage_evidence_window_synced(env) -> bool:
    return (
        stage_read_result_groups(env, 23, 'notification_hub', ('get_notification',), [('notif_outage_stage23',), ('water outage', 'repair')])
        and tool_stage_any(env, 23, 'notion', [('water outage', 'repair'), ('evidence', 'photography')])
    )

CHECKS = [
    ('s23_water_outage_calendar_updated', s23_water_outage_calendar_updated, 1.5),
    ('s23_outage_evidence_window_synced', s23_outage_evidence_window_synced, 1.25),
]
