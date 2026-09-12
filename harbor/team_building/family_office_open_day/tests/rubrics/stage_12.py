from __future__ import annotations
from ._helpers import *


def s12_traffic_backup_pickup(env) -> bool:
    photo_recheck = used(env, 12, "email", "search") or used(env, 12, "email", "get")
    boundary_record = stage_persisted(env, 12, [["photography", "authorization"], ["default", "decline"], ["publish"], ["Han", "confirmation"]])
    return photo_recheck and boundary_record


CHECKS = [
    ("s12_traffic_backup_pickup", s12_traffic_backup_pickup, 1.75),
]
