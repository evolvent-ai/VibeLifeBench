from __future__ import annotations
from ._helpers import *

def s27_final_archive_refreshed(env) -> bool:
    return (
        stage_servers_at_least(env, 27, 5)
        and tool_stage_any(env, 27, 'email', [('thread_landlord_renewal', 'lease renewal'), ('non-renewal', 'quote')])
        and tool_stage_any(env, 27, 'listing_platform', [('lst_tj_1901', '1901'), ('lst_tj_1906', '1906')])
        and tool_stage_any(env, 27, 'notion', [('open items', 'next step'), ('ranking', 'candidate')])
        and workspace_file_has_groups(env, 'FINAL_REVIEW.md', [('lease renewal',), ('relocation',), ('requires user confirmation',)])
    )

def s27_final_authorization_open_items_refreshed(env) -> bool:
    return (
        tool_stage_any(env, 27, 'calendar', [('2026-08-07', 'expiry'), ('water outage', 'viewing')])
        and tool_stage_any(env, 27, 'notification_hub', [('water outage', 'damp mark'), ('repair', 'handover')])
        and tool_stage_any(env, 27, 'notion', [('payment', 'signing'), ('open items', 'authorization')])
        and workspace_file_has_groups(env, 'AUTH_LOG.md', [('payment',), ('signing',), ('status',)])
    )

def s27_closure_source_matrix_fresh(env) -> bool:
    return (
        stage_servers_at_least(env, 27, 4)
        and stage_matrix_at_least(env, 27, [
            ('email', [('thread_landlord_renewal', 'lease renewal', 'landlord'), ('non-renewal', 'quote')]),
            ('listing_platform', [('lst_tj_1901', '1901'), ('lst_tj_1906', '1906'), ('candidate', 'listing')]),
            ('calendar', [('2026-08-07', 'expiry'), ('water outage', 'viewing')]),
            ('notification_hub', [('water outage', 'damp mark'), ('repair', 'handover')]),
            ('notion', [('open items', 'next step'), ('authorization', 'ranking')]),
        ], 3)
        and workspace_file_has_groups(env, 'HEARTBEAT.md', [('quote',), ('repair',), ('listing',), ('route',)])
    )

CHECKS = [
    ('s27_final_archive_refreshed', s27_final_archive_refreshed, 1.75),
    ('s27_final_authorization_open_items_refreshed', s27_final_authorization_open_items_refreshed, 1.25),
    ('s27_closure_source_matrix_fresh', s27_closure_source_matrix_fresh, 1.0),
]
