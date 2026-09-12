from __future__ import annotations
from ._helpers import *

def s16_pipe_check_not_completed(env) -> bool:
    return (
        stage_read_result_groups(env, 16, 'notification_hub', ('get_notification',), [('notif_pipe_stage16',), ('planned', 'no repair result', 'not confirmed')])
        and tool_stage_any(env, 16, 'notion', [('incomplete', 'not complete', 'not confirmed', 'pending'), ('pipe', 'repair', 'inspection')])
    )

CHECKS = [
    ('s16_pipe_check_not_completed', s16_pipe_check_not_completed, 1.5),
]
