from __future__ import annotations
from ._helpers import *

def s1_update_goal_constraints(env) -> bool:
    checked_mail = used(env, 1, "email", "search") or used(env, 1, "email", "get")
    persisted = stage_persisted(env, 1, [["family-friendly", "belonging"], ["childcare", "talent"], ["office", "safety"]])
    return checked_mail and persisted

CHECKS = [
    ('s1_update_goal_constraints', s1_update_goal_constraints, 1.5),
]
