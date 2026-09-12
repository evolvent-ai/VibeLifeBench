from __future__ import annotations
from ._helpers import *

def s15_quiet_gap_refresh(env) -> bool:
    return (
        stage_read_result_groups(env, 15, 'notification_hub', ('list_notifications',), [('property', 'listing')])
        and tool_stage(env, 15, 'listing_platform', None, ['lst_tj_1901'])
        and stage_read_email_ids(env, 15, ('1', '231'))
    )

CHECKS = [
    ('s15_quiet_gap_refresh', s15_quiet_gap_refresh, 1.5),
]
