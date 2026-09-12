from __future__ import annotations
from ._helpers import *

def s21_core_candidate_cross_checked(env) -> bool:
    return (
        stage_route_within_minutes(env, 21, 'lst_tj_1901', 49)
        and tool_stage_any(env, 21, 'listing_platform', [('lst_tj_1901', '1901'), ('active', 'candidate')])
        and workspace_file_has_groups(env, 'MOVE_CANDIDATE_TRACKER.md', [('lst_tj_1901',), ('commute',), ('status',)])
    )

def s21_candidate_triangulation_recorded(env) -> bool:
    return stage_matrix_at_least(env, 21, [
        ('listing_platform', [('lst_tj_1901', '1901'), ('lst_tj_1906', '1906')]),
        ('maps', [('current_home',), ('lst_tj_1901', '1901')]),
        ('review_platform', [('mer_tj_community_1901', '1901'), ('mer_tj_community_1906', '1906')]),
        ('notion', [('candidate', 'ranking'), ('commute', 'review')]),
    ], 3) and workspace_file_has_groups(env, 'MOVE_CANDIDATE_TRACKER.md', [('candidate',), ('commute',), ('review',)])

def s21_candidate_minimum_refresh(env) -> bool:
    return stage_matrix_at_least(env, 21, [
        ('listing_platform', [('lst_tj_1901', '1901'), ('lst_tj_1906', '1906')]),
        ('maps', [('current_home',), ('lst_tj_1901', '1901')]),
        ('review_platform', [('mer_tj_community_1901', '1901'), ('mer_tj_community_1906', '1906')]),
        ('notion', [('candidate', 'ranking'), ('commute', 'review')]),
    ], 2) and workspace_file_has_groups(env, 'HEARTBEAT.md', [('listing',), ('route',), ('next review',)])

CHECKS = [
    ('s21_core_candidate_cross_checked', s21_core_candidate_cross_checked, 1.5),
    ('s21_candidate_triangulation_recorded', s21_candidate_triangulation_recorded, 1.0),
    ('s21_candidate_minimum_refresh', s21_candidate_minimum_refresh, 1.0),
]
