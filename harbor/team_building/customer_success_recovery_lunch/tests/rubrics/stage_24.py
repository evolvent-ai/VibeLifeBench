from __future__ import annotations
from ._helpers import *

def s24_final_archive_sop(env) -> bool:
    return any_write(env, 24) and state_has(env, 24, [['review'], ['psychological'], ['budget'], ['vendor'], ['SOP']])

CHECKS = [
    ('s24_final_archive_sop', s24_final_archive_sop, 1.5),
]
