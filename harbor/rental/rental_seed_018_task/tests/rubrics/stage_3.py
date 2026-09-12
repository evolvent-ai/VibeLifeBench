from __future__ import annotations
from ._helpers import *

def s3_commute_crosscheck_a_c(env) -> bool:
    return (
        tool_stage(env, 3, 'maps', None, [C.HOSPITAL])
        and (tool_stage(env, 3, 'maps', None, [C.PLACE_A]) or tool_stage(env, 3, 'maps', None, [C.PLACE_C]))
        and stage_reply_has_any(env, 3, [['walking'], ['transfer'], ['door-to-door'], ['morning'], ['commute']])
    )

def s3_market_price_check(env) -> bool:
    return (
        tool_stage_any(env, 3, [
            ('listing_platform', 'market', ['Qinghe Lanting']),
            ('listing_platform', 'market', ['Chaoyangli']),
            ('listing_platform', 'market', ['Jingcheng Anju']),
            ('listing_platform', 'market', ['Donghu New Residence']),
        ])
        and listing_price(env, C.LIST_B) <= 900000
        and stage_reply_has_any(env, 3, [['comparison'], ['market'], ['average'], ['budget'], ['price']])
    )

CHECKS = [
    ('s3_commute_crosscheck_a_c', s3_commute_crosscheck_a_c, 1.5),
    ('s3_market_price_check', s3_market_price_check, 1.25),
]
