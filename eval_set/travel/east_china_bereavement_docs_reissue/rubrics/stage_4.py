from __future__ import annotations
from ._helpers import check_s4_schedule_temp_id_buffer

def s4_schedule_temp_id_buffer(env) -> bool:
    return check_s4_schedule_temp_id_buffer(env)

CHECKS = [
    ("s4_schedule_temp_id_buffer", s4_schedule_temp_id_buffer, 1),
]
