from __future__ import annotations
from ._helpers import check_s13_appointment_change_update

def s13_appointment_change_update(env) -> bool:
    return check_s13_appointment_change_update(env)

CHECKS = [
    ("s13_appointment_change_update", s13_appointment_change_update, 2),
]
