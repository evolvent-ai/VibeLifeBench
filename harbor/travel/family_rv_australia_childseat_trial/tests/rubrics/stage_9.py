from __future__ import annotations
from ._helpers import *

def s9_calendar_driving_segments(env) -> bool:
    return _calendar_write_in_stage(env, 9) and _has_calendar(env, [['sydney', 'Sydney'], ['canberra', 'Canberra'], ['albury', 'melbourne', 'Melbourne'], ['recovery', 'rest']])

def s9_no_segment_over_limit(env) -> bool:
    return _check_text(env, 9, [['3.5', 'duration', '4h', 'hours'], ['night', 'no night'], ['recovery', 'rest']])

def s9_right_hand_adaptation_block(env) -> bool:
    return _calendar_write_in_stage(env, 9) and _has_calendar(env, [['right-hand-drive', 'right-hand'], ['adaptation', 'practice', 'low-speed']]) and _workspace_file_has(env, FILE_ROUTE_PLAN, [['right-hand-drive', 'right-hand'], ['adaptation', 'practice', 'low-speed'], ['night', 'no night'], ['recovery', 'rest']])
CHECKS = [('s9_calendar_driving_segments', s9_calendar_driving_segments, 2.0), ('s9_no_segment_over_limit', s9_no_segment_over_limit, 2.0), ('s9_right_hand_adaptation_block', s9_right_hand_adaptation_block, 2.0)]
