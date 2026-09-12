from __future__ import annotations
from ._helpers import _check

def chk_s06_calendar_mutation_discovered(env) -> bool:
    return _check('chk_s06_calendar_mutation_discovered', env)

def chk_s06_diff_refresh_calendar_after_mutation(env) -> bool:
    return _check('chk_s06_diff_refresh_calendar_after_mutation', env)

CHECKS = [
    ('chk_s06_calendar_mutation_discovered', chk_s06_calendar_mutation_discovered, 1.75),
    ('chk_s06_diff_refresh_calendar_after_mutation', chk_s06_diff_refresh_calendar_after_mutation, 1.5),
]
