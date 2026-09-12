from __future__ import annotations
from ._helpers import *

def s8_scheduled_multi_server_check(env) -> bool:
    return (
        used(env, 8, 'review_platform')
        and stage_server_hits(env, 8, [('calendar', None), ('maps', None), ('notion', None), ('notification_hub', None)]) >= 2
        and any_write(env, 8)
        and state_has(env, 8, [['voluntary', 'low-pressure', 'psychological', 'opt out'], ['safety', 'catering', 'coverage']])
    )

CHECKS = [
    ('s8_scheduled_multi_server_check', s8_scheduled_multi_server_check, 1.5),
]
