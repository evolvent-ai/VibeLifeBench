from __future__ import annotations
from ._helpers import *

def s24_1906_discount_conflict_handled(env) -> bool:
    return (
        tool_stage(env, 24, 'listing_platform', 'get_listing_detail', ['lst_tj_1906', '565000', '2026-08-05'])
        and stage_read_result_groups(env, 24, 'calendar', ('list_events',), [('cal_month_end_close',), ('2026-08-05',), ('09:00',), ('11:00',)])
        and listing_price(env, C.LIST_1906) == 565000
        and listing_attr(env, C.LIST_1906, 'view_window') == '2026-08-05T10:00:00+08:00'
        and calendar_event_exact(env, [('close', 'financial')], '2026-08-05T09:00', '2026-08-05T11:00')
    )

def s24_discount_conflict_calendar_synced(env) -> bool:
    return (
        tool_stage(env, 24, 'listing_platform', 'get_listing_detail', ['lst_tj_1906', '565000', '2026-08-05'])
        and stage_read_result_groups(env, 24, 'calendar', ('list_events',), [('cal_month_end_close',), ('2026-08-05',)])
        and tool_stage_any(env, 24, 'notion', [('lst_tj_1906', '1906'), ('conflict', 'conditional alternative')])
    )

def s24_discount_exact_window_recorded(env) -> bool:
    return (
        listing_price(env, C.LIST_1906) == 565000
        and listing_attr(env, C.LIST_1906, 'view_window') == '2026-08-05T10:00:00+08:00'
        and stage_matrix_at_least(env, 24, [
            ('listing_platform', [('lst_tj_1906', '1906'), ('565000',), ('2026-08-05',)]),
            ('calendar', [('cal_month_end_close',), ('2026-08-05',)]),
            ('notion', [('lst_tj_1906', '1906'), ('5650', '565000', 'price reduction'), ('window', 'conflict')]),
        ], 3)
    )

CHECKS = [
    ('s24_1906_discount_conflict_handled', s24_1906_discount_conflict_handled, 1.75),
    ('s24_discount_conflict_calendar_synced', s24_discount_conflict_calendar_synced, 1.25),
    ('s24_discount_exact_window_recorded', s24_discount_exact_window_recorded, 1.0),
]
