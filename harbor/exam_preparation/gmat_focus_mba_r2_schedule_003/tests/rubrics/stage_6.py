from __future__ import annotations
from . import _helpers as H

def s6_harbor_deadline_recovered(env) -> bool:
    return H.s6_harbor_deadline_recovered(env)

def s6_harbor_calendar_updated(env) -> bool:
    return H.s6_harbor_calendar_updated(env)

CHECKS = [
    ("s6_harbor_deadline_recovered", s6_harbor_deadline_recovered, 1.75),
    ("s6_harbor_calendar_updated", s6_harbor_calendar_updated, 1.5)
]
