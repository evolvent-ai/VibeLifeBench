from __future__ import annotations
from ._helpers import check_s15_return_flight_reason

def s15_return_flight_reason(env) -> bool:
    return check_s15_return_flight_reason(env)

CHECKS = [
    ("s15_return_flight_reason", s15_return_flight_reason, 3),
]
