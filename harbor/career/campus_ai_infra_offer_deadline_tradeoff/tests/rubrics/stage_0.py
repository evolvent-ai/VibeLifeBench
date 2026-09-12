from __future__ import annotations

from ._helpers import _check


def stage_00_initialize_tracker(env) -> bool:
    return _check('stage_00_initialize_tracker', env)


def stage_00_salary_rules_and_authorization_recorded(env) -> bool:
    return _check('stage_00_salary_rules_and_authorization_recorded', env)


def stage_00_no_forbidden_action(env) -> bool:
    return _check('stage_00_no_forbidden_action', env)


CHECKS = [
    ('stage_00_initialize_tracker', stage_00_initialize_tracker, 1.5),
    ('stage_00_salary_rules_and_authorization_recorded', stage_00_salary_rules_and_authorization_recorded, 2.0),
    ('stage_00_no_forbidden_action', stage_00_no_forbidden_action, 2.0),
]
