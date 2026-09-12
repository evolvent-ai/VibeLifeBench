from __future__ import annotations
from ._helpers import *

def s13_instructor_reverify(env) -> bool:
    read_update = used(env, 13, "email", "search") or used(env, 13, "email", "get")
    followup = stage_persisted(env, 13, [["instructor"], ["insurance", "credentials"], ["delay", "pending"], ["recheck", "confirmation"]])
    return read_update and followup

CHECKS = [
    ('s13_instructor_reverify', s13_instructor_reverify, 1.5),
]
