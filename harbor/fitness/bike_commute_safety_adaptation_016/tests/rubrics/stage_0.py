from __future__ import annotations
from ._helpers import _check

def chk_s00_briefing_capture(env) -> bool:
    return _check('chk_s00_briefing_capture', env)

def chk_s00_initial_assets(env) -> bool:
    return _check('chk_s00_initial_assets', env)

CHECKS = [
    ('chk_s00_briefing_capture', chk_s00_briefing_capture, 1.25),
    ('chk_s00_initial_assets', chk_s00_initial_assets, 1.0),
]
