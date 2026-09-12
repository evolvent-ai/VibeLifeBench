from __future__ import annotations
from ._helpers import *

def s17_alternative_candidate_pool(env) -> bool:
    return bool(
        tool_stage(env, 17, 'listing_platform', 'search', ('850000',))
        and tool_stage_object(env, 17, 'listing_platform', None, C.LIST_E, ('Xierqi Zhixueyuan',))
        and tool_stage_object(env, 17, 'maps', None, C.PLACE_E, ('Xierqi Zhixueyuan',))
        and listing_status(env, C.LIST_E) == 'active'
        and listing_price(env, C.LIST_E) == 748000
        and place_has_parts(env, C.PLACE_E, ('Xierqi Zhixueyuan', 'closes_22_30'))
        and saved_has(env, C.LIST_E)
        and derived_stage_has(env, 17, (C.LIST_E, '748000', 'pending confirmation'), ('CANDIDATE_TRACKER.md', 'RISK_LOG.md'))
    )

def s17_calendar_window_draft_only(env) -> bool:
    return bool(
        tool_stage(env, 17, 'calendar', None, ('Xierqi Zhixueyuan', 'internal'))
        and calendar_has_event_parts(env, ('Xierqi Zhixueyuan', 'internal'), '2026-08-03T00:00:00+08:00', '2026-08-07T23:59:59+08:00')
        and positive_authorization_boundary(env, 17, ('home viewing', 'confirmation'))
        and len(viewings(env)) == 0
    )

CHECKS = [
    ("s17_alternative_candidate_pool", s17_alternative_candidate_pool, 1.25),
    ("s17_calendar_window_draft_only", s17_calendar_window_draft_only, 1.5),
]
