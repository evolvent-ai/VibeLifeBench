from __future__ import annotations

from ._helpers import _check


def stage_06_conflict_and_reschedule_options_prepared(env) -> bool:
    return _check('stage_06_conflict_and_reschedule_options_prepared', env)


CHECKS = [
    ('stage_06_conflict_and_reschedule_options_prepared', stage_06_conflict_and_reschedule_options_prepared, 2.0),
]
