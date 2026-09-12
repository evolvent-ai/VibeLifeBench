from __future__ import annotations
from ._helpers import *

def s3_commute_crosscheck_current_backup(env) -> bool:
    return bool(
        tool_stage_object(env, 3, 'maps', None, C.PLACE_A, ('Qinghe Jiayuan',))
        and tool_stage_object(env, 3, 'maps', None, C.PLACE_C, ('Qinghe Alternative Residence',))
        and place_has_parts(env, C.PLACE_A, ('Qinghe Jiayuan', 'Beijing'))
        and place_has_parts(env, C.PLACE_C, ('Qinghe Alternative Residence', 'Beijing'))
        and tool_stage_group(env, 3, 'listing_platform', 'market', [('Qinghe Jiayuan',), ('Qinghe Alternative Residence',)])
        and market_has_current_rent(env, 'Qinghe Jiayuan')
        and market_has_current_rent(env, 'Qinghe Alternative Residence')
        and derived_stage_has(env, 3, ('door-to-door', 'walking', 'transfers'), ('CANDIDATE_TRACKER.md',))
    )

def s3_market_price_check(env) -> bool:
    return bool(
        tool_stage_group(env, 3, 'listing_platform', 'market', [('Qinghe Jiayuan',), ('Qinghe Alternative Residence',), ('Haidian District',)])
        and market_has_current_rent(env, 'Haidian District')
        and derived_stage_has(env, 3, ('market', 'avg_price_minor', 'sample_size'), ('BUDGET_LEDGER.md', 'CANDIDATE_TRACKER.md'))
    )

CHECKS = [
    ("s3_commute_crosscheck_current_backup", s3_commute_crosscheck_current_backup, 1.5),
    ("s3_market_price_check", s3_market_price_check, 1.25),
]
