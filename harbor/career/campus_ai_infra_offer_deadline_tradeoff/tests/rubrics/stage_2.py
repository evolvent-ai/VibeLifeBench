from __future__ import annotations

from ._helpers import _check


def stage_02_core_jobs_and_review_reminder_created(env) -> bool:
    return _check('stage_02_core_jobs_and_review_reminder_created', env)


CHECKS = [
    ('stage_02_core_jobs_and_review_reminder_created', stage_02_core_jobs_and_review_reminder_created, 2.0),
]
