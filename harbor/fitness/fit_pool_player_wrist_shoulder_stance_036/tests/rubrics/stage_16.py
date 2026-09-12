from __future__ import annotations
from ._helpers import _check

def chk_s16_venue_fatigue_risk_logged(env) -> bool:
    return _check('chk_s16_venue_fatigue_risk_logged', env)

CHECKS = [
    ('chk_s16_venue_fatigue_risk_logged', chk_s16_venue_fatigue_risk_logged, 1.25),
]
