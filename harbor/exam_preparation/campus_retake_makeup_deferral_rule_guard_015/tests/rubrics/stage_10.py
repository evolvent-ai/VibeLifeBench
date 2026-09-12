from . import _helpers as h

def s10_room_update_detected(env):
    return h.s10_room_update_detected(env)

def s10_room_update_calendar_same_stage(env):
    return h.s10_room_update_calendar_same_stage(env)

def s10_room_update_evidence_same_stage(env):
    return h.s10_room_update_evidence_same_stage(env)

CHECKS = [
    ("s10_room_update_detected", s10_room_update_detected, 1.5),
    ("s10_room_update_calendar_same_stage", s10_room_update_calendar_same_stage, 1.0),
    ("s10_room_update_evidence_same_stage", s10_room_update_evidence_same_stage, 1.0),
]
