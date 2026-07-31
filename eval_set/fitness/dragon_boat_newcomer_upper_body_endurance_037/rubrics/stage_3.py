from __future__ import annotations
from ._helpers import _check

def chk_s03_venue_candidate_table(env) -> bool:
    return _check('chk_s03_venue_candidate_table', env)

CHECKS = [
    ('chk_s03_venue_candidate_table', chk_s03_venue_candidate_table, 1.25)
]
