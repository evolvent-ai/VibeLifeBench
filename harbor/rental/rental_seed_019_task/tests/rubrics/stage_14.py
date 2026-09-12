from __future__ import annotations
from ._helpers import *

def s14_delisted_removed(env) -> bool:
    return tool_stage(env, 14, 'listing_platform', None, ['lst_tj_1905']) and listing_status(env, C.LIST_1905) == 'delisted'

def s14_calendar_synced_after_delist(env) -> bool:
    delist_groups = [
        ('lst_tj_1905', '1905', 'Cultural Center'),
        ('delisted', 'delisted', 'invalid', 'remove', 'cancel'),
        ('viewing', 'candidate', 'hold', 'review'),
    ]
    return (
        listing_status(env, C.LIST_1905) == 'delisted'
        and stage_calendar_write(env, 14, delist_groups)
        and calendar_event_has_groups(env, delist_groups)
    )

CHECKS = [
    ('s14_delisted_removed', s14_delisted_removed, 1.75),
    ('s14_calendar_synced_after_delist', s14_calendar_synced_after_delist, 1.5),
]
