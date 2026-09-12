from __future__ import annotations
from ._helpers import check_s17_pickup_low_sensitive

def s17_pickup_low_sensitive(env) -> bool:
    return check_s17_pickup_low_sensitive(env)

CHECKS = [
    ("s17_pickup_low_sensitive", s17_pickup_low_sensitive, 3),
]
