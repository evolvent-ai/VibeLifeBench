from __future__ import annotations

from ._helpers import check_by_id

def stage_03_agency_noise_downgraded(env) -> bool:
    return check_by_id(env, 'stage_03_agency_noise_downgraded')

CHECKS = [
    ('stage_03_agency_noise_downgraded', stage_03_agency_noise_downgraded, 1.0),
]
