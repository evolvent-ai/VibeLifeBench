from __future__ import annotations
from ._helpers import *

def s21_return_route_accessible(env) -> bool:
    # event-021 says "opening a second paper-circuit group", "wristband colors"
    # and "the line ... has grown"; match those spellings too.
    action = stage_persisted(env, 21, [["second-group", "second group", "second"], ["paper-circuit"], ["wristbands", "wristband"], ["queue", "line"]])
    return action

CHECKS = [
    ('s21_return_route_accessible', s21_return_route_accessible, 1.75),
]
