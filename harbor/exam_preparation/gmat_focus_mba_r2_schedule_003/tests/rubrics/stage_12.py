from __future__ import annotations
from . import _helpers as H

def s12_scheduled_heartbeat_checked(env) -> bool:
    return H.s12_scheduled_heartbeat_checked(env)

def s12_confirmation_calendar_present(env) -> bool:
    return H.s12_confirmation_calendar_present(env)

CHECKS = [
    ("s12_scheduled_heartbeat_checked", s12_scheduled_heartbeat_checked, 1.25),
    ("s12_confirmation_calendar_present", s12_confirmation_calendar_present, 1.25)
]
