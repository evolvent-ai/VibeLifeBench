from __future__ import annotations
from ._helpers import _check

def chk_s08_mutation_precheck_discovery(env) -> bool:
    return _check('chk_s08_mutation_precheck_discovery', env)

def chk_s08_commute_trial_rescheduled(env) -> bool:
    return _check('chk_s08_commute_trial_rescheduled', env)

def chk_s08_no_work_meeting_cancelled(env) -> bool:
    return _check('chk_s08_no_work_meeting_cancelled', env)

CHECKS = [
    ('chk_s08_mutation_precheck_discovery', chk_s08_mutation_precheck_discovery, 1.75),
    ('chk_s08_commute_trial_rescheduled', chk_s08_commute_trial_rescheduled, 2.0),
    ('chk_s08_no_work_meeting_cancelled', chk_s08_no_work_meeting_cancelled, 2.0),
]
