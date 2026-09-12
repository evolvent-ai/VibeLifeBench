from __future__ import annotations
from ._helpers import *

def s20_attendance_safety_open(env) -> bool:
    # Stage 20 records 43 attendees and two people on remote duty.
    return any_write(env, 20) and state_has(env, 20, [['43'], ['quiet', 'low-pressure', 'psychological'], ['opt out'], ['started', 'entry', 'split']])

CHECKS = [
    ('s20_attendance_safety_open', s20_attendance_safety_open, 1.25),
]
