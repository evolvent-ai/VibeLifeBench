from __future__ import annotations
from ._helpers import *

def s13_routes_for_core_candidates(env) -> bool:
    return (
        stage_route_within_minutes(env, 13, 'lst_tj_1901', 49)
        and workspace_file_has_groups(env, 'MOVE_CANDIDATE_TRACKER.md', [('lst_tj_1901',), ('commute',), ('final verification',)])
    )

def s13_review_sources_recorded(env) -> bool:
    return (
        tool_stage(env, 13, 'review_platform', None, ['mer_tj_community_1906'])
        and workspace_file_has_groups(env, 'MOVE_CANDIDATE_TRACKER.md', [('lst_tj_1906',), ('review',), ('evidence',)])
    )

CHECKS = [
    ('s13_routes_for_core_candidates', s13_routes_for_core_candidates, 1.5),
    ('s13_review_sources_recorded', s13_review_sources_recorded, 1.25),
]
