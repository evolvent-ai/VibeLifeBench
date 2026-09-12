from __future__ import annotations
from ._helpers import *

def s20_attendance_access_path(env) -> bool:
    onsite_record = stage_persisted(env, 20, [["59"], ["34"], ["isolation"], ["server", "Finance"]])
    return onsite_record

CHECKS = [
    ('s20_attendance_access_path', s20_attendance_access_path, 1.25),
]
