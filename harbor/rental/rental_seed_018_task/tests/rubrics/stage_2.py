from __future__ import annotations
from ._helpers import *

def s2_scheduled_monitor_setup(env) -> bool:
    return (
        tool_stage(env, 2, 'notification_hub', 'list_subscriptions', [C.USER])
        and tool_stage(env, 2, 'calendar', 'create_event', ['status', 'fee'])
        and calendar_has_event_parts(env, ['status', 'fee'])
        and stage_reply_has_any(env, 2, [['monitor'], ['review'], ['recurring'], ['pending'], ['tracking']])
    )

def s2_tracker_persisted(env) -> bool:
    return (
        s2_scheduled_monitor_setup(env)
        and tool_stage(env, 2, 'notion', None, [C.LIST_B])
        and notion_has_parts(env, [C.LIST_B])
    )

CHECKS = [
    ('s2_scheduled_monitor_setup', s2_scheduled_monitor_setup, 1.25),
    ('s2_tracker_persisted', s2_tracker_persisted, 1.25),
]
