from __future__ import annotations
from ._helpers import _check

def chk_s04_calendar_plan_created(env) -> bool:
    return _check('chk_s04_calendar_plan_created', env)

def chk_s04_table_pre_post_routine(env) -> bool:
    return _check('chk_s04_table_pre_post_routine', env)

def chk_s04_notification_subscriptions(env) -> bool:
    return _check('chk_s04_notification_subscriptions', env)

CHECKS = [
    ('chk_s04_calendar_plan_created', chk_s04_calendar_plan_created, 1.5),
    ('chk_s04_table_pre_post_routine', chk_s04_table_pre_post_routine, 1.25),
    ('chk_s04_notification_subscriptions', chk_s04_notification_subscriptions, 1.25),
]
