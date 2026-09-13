from __future__ import annotations
from ._helpers import *

def s20_attendance_access_path(env) -> bool:
    # event-020 spells out "Fifty-nine" and describes the access control as
    # "barrier tape ... around the server room and financial-records area".
    onsite_record = stage_persisted(env, 20, [["59", "fifty-nine"], ["34"], ["isolation", "barrier tape", "restricted"], ["server", "Finance"]])
    return onsite_record

CHECKS = [
    ('s20_attendance_access_path', s20_attendance_access_path, 1.25),
]
