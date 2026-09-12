from __future__ import annotations
from ._helpers import _check

def chk_s02_calendar_windows_identified(env) -> bool:
    return _check('chk_s02_calendar_windows_identified', env)

def chk_s02_notification_hub_seen(env) -> bool:
    return _check('chk_s02_notification_hub_seen', env)

CHECKS = [
    ('chk_s02_calendar_windows_identified', chk_s02_calendar_windows_identified, 1.25),
    ('chk_s02_notification_hub_seen', chk_s02_notification_hub_seen, 1.25),
]
