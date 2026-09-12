from __future__ import annotations
from ._helpers import *

def s9_quote_6050_discovered(env) -> bool:
    return (
        stage_read_email_ids(env, 9, ('231',))
        and email_search_has(env, '6050', ('231',), folder='INBOX')
    )

def s9_deadline_calendar_updated(env) -> bool:
    quote_groups = [
        ('6050', '6,050', '6050'),
        ('lease renewal', 'rent increase', 'quote'),
        ('reply', 'deadline', 'deadline', 'deadline'),
    ]
    return stage_calendar_write(env, 9, quote_groups) and calendar_event_has_groups(env, quote_groups)

CHECKS = [
    ('s9_quote_6050_discovered', s9_quote_6050_discovered, 1.75),
    ('s9_deadline_calendar_updated', s9_deadline_calendar_updated, 1.5),
]
