from __future__ import annotations
from . import _helpers as H

def s3_seat_calendar_scanned(env) -> bool:
    return H.s3_seat_calendar_scanned(env)

def s3_seat_candidates_saved(env) -> bool:
    return H.s3_seat_candidates_saved(env)

CHECKS = [
    ("s3_seat_calendar_scanned", s3_seat_calendar_scanned, 1.5),
    ("s3_seat_candidates_saved", s3_seat_candidates_saved, 1.25)
]
