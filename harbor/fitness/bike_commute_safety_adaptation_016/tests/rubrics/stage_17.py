from __future__ import annotations
from ._helpers import _check

def chk_s17_late_event_no_night_ride(env) -> bool:
    return _check('chk_s17_late_event_no_night_ride', env)

CHECKS = [
    ('chk_s17_late_event_no_night_ride', chk_s17_late_event_no_night_ride, 1.75),
]
