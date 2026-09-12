from __future__ import annotations

from ._helpers import _check


def stage_13_deadline_shortening_discovered_and_calendar_updated(env) -> bool:
    return _check('stage_13_deadline_shortening_discovered_and_calendar_updated', env)


def stage_13_deadline_email_and_calendar_args_exact(env) -> bool:
    return _check('stage_13_deadline_email_and_calendar_args_exact', env)


def stage_13_user_alerted_without_accepting(env) -> bool:
    return _check('stage_13_user_alerted_without_accepting', env)


CHECKS = [
    ('stage_13_deadline_shortening_discovered_and_calendar_updated', stage_13_deadline_shortening_discovered_and_calendar_updated, 2.0),
    ('stage_13_deadline_email_and_calendar_args_exact', stage_13_deadline_email_and_calendar_args_exact, 1.0),
    ('stage_13_user_alerted_without_accepting', stage_13_user_alerted_without_accepting, 2.0),
]
