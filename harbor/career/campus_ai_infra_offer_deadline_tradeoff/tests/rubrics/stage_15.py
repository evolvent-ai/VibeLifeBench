from __future__ import annotations

from ._helpers import _check


def stage_15_advisor_constraint_calendar_and_start_date_recorded(env) -> bool:
    return _check('stage_15_advisor_constraint_calendar_and_start_date_recorded', env)


CHECKS = [
    ('stage_15_advisor_constraint_calendar_and_start_date_recorded', stage_15_advisor_constraint_calendar_and_start_date_recorded, 1.75),
]
