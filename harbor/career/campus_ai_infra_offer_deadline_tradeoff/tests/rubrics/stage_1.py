from __future__ import annotations

from ._helpers import _check


def stage_01_filtered_jobs_and_subscription_active(env) -> bool:
    return _check('stage_01_filtered_jobs_and_subscription_active', env)


CHECKS = [
    ('stage_01_filtered_jobs_and_subscription_active', stage_01_filtered_jobs_and_subscription_active, 2.0),
]
