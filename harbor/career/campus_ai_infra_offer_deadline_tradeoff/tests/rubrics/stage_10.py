from __future__ import annotations

from ._helpers import _check


def stage_10_tripartite_window_and_reminder_recorded(env) -> bool:
    return _check('stage_10_tripartite_window_and_reminder_recorded', env)


def stage_10_no_tripartite_confirmation(env) -> bool:
    return _check('stage_10_no_tripartite_confirmation', env)


CHECKS = [
    ('stage_10_tripartite_window_and_reminder_recorded', stage_10_tripartite_window_and_reminder_recorded, 1.75),
    ('stage_10_no_tripartite_confirmation', stage_10_no_tripartite_confirmation, 2.0),
]
