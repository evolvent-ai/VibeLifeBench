from __future__ import annotations
from ._helpers import *

def s20_price_window_refresh(env) -> bool:
    return (
        tool_stage(env, 20, 'listing_platform', 'get_listing_detail', ['lst_tj_1902', '579000'])
        and listing_price(env, C.LIST_1902) == 579000
        and workspace_file_has_groups(env, 'MOVE_CANDIDATE_TRACKER.md', [('lst_tj_1902',), ('5790', '579000'), ('monthly rent',), ('final verification',)])
    )

CHECKS = [
    ('s20_price_window_refresh', s20_price_window_refresh, 1.75),
]
