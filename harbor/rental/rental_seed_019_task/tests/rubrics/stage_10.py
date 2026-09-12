from __future__ import annotations
from ._helpers import *

def s10_candidate_pool_saved(env) -> bool:
    return (
        tool_stage(env, 10, 'listing_platform', None, ['lst_tj_1901'])
        and saved_has(env, C.LIST_1901)
        and workspace_file_has_groups(env, 'MOVE_CANDIDATE_TRACKER.md', [('lst_tj_1901',), ('status',), ('next step',)])
    )

def s10_unknowns_marked(env) -> bool:
    return tool_stage_any(env, 10, 'notion', [('unknown', 'unverified', 'not yet known'), ('pending verification', 'awaiting verification', 'requires verification')])

CHECKS = [
    ('s10_candidate_pool_saved', s10_candidate_pool_saved, 1.5),
    ('s10_unknowns_marked', s10_unknowns_marked, 1.25),
]
