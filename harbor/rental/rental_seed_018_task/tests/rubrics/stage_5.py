from __future__ import annotations
from ._helpers import *

def s5_night_shift_recheck(env) -> bool:
    return (
        tool_stage_any(env, 5, [
            ('maps', None, [C.PLACE_A]),
            ('maps', None, [C.PLACE_B]),
            ('maps', None, [C.PLACE_C]),
        ])
        and tool_stage(env, 5, 'calendar', None)
        and stage_reply_has_any(env, 5, [['commute'], ['door-to-door'], ['morning'], ['fee'], ['registration']])
    )

def s5_roommate_and_elevator_risk(env) -> bool:
    return (
        tool_stage_any(env, 5, [
            ('listing_platform', None, [C.LIST_A]),
            ('listing_platform', None, [C.LIST_B]),
            ('listing_platform', None, [C.LIST_C]),
        ])
        and tool_stage_any(env, 5, [
            ('review_platform', None, [C.MER_A]),
            ('review_platform', None, [C.MER_B]),
            ('review_platform', None, [C.MER_C]),
        ])
        and stage_reply_has_any(env, 5, [['elevator'], ['natural'], ['management'], ['risk'], ['review']])
    )

CHECKS = [
    ('s5_night_shift_recheck', s5_night_shift_recheck, 1.5),
    ('s5_roommate_and_elevator_risk', s5_roommate_and_elevator_risk, 1.25),
]
