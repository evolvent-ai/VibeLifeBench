from __future__ import annotations
from ._helpers import *

def s6_reviews_used_as_clues(env) -> bool:
    return stage_read_result_groups(env, 6, 'review_platform', ('list_reviews',), [('mer_tj_community_1901',)]) and tool_stage(env, 6, 'notion', None, ['clue'])

def s6_property_notice_read(env) -> bool:
    return (
        stage_read_result_groups(env, 6, 'notification_hub', ('list_notifications',), [('property',), ('property management', 'inspection', 'repair')])
        and tool_stage(env, 6, 'notion', None, ['property management'])
        and workspace_file_has_groups(env, 'REPAIR_EVIDENCE_INDEX.md', [('property management',), ('source',), ('repair status',)])
    )

CHECKS = [
    ('s6_reviews_used_as_clues', s6_reviews_used_as_clues, 1.25),
    ('s6_property_notice_read', s6_property_notice_read, 1.25),
]
