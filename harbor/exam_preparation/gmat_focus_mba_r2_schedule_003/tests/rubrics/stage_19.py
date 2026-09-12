from __future__ import annotations
from . import _helpers as H

def s19_unofficial_recorded_no_send(env) -> bool:
    return H.s19_unofficial_recorded_no_send(env)

def s19_no_score_send_on_unofficial(env) -> bool:
    return H.s19_no_score_send_on_unofficial(env)

CHECKS = [
    ("s19_unofficial_recorded_no_send", s19_unofficial_recorded_no_send, 1.75),
    ("s19_no_score_send_on_unofficial", s19_no_score_send_on_unofficial, 2.0)
]
