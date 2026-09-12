from __future__ import annotations
from ._helpers import _check

def chk_s00_briefing_capture(env) -> bool:
    return _check('chk_s00_briefing_capture', env)

def chk_s00_initial_logs(env) -> bool:
    return _check('chk_s00_initial_logs', env)

CHECKS = [
    ('chk_s00_briefing_capture', chk_s00_briefing_capture, 1.5),
    ('chk_s00_initial_logs', chk_s00_initial_logs, 1.25),
]
