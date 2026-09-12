from __future__ import annotations
from ._helpers import *

def s21_return_route_accessible(env) -> bool:
    action = stage_persisted(env, 21, [["second-group"], ["paper-circuit"], ["wristbands"], ["queue"]])
    return action

CHECKS = [
    ('s21_return_route_accessible', s21_return_route_accessible, 1.75),
]
