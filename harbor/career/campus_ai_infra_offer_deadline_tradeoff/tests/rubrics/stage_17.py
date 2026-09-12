from __future__ import annotations

from ._helpers import _check


def stage_17_extension_and_start_date_recorded(env) -> bool:
    return _check('stage_17_extension_and_start_date_recorded', env)


def stage_17_extension_reply_and_calendar_args_exact(env) -> bool:
    return _check('stage_17_extension_reply_and_calendar_args_exact', env)


def stage_17_offer_not_accepted(env) -> bool:
    return _check('stage_17_offer_not_accepted', env)


CHECKS = [
    ('stage_17_extension_and_start_date_recorded', stage_17_extension_and_start_date_recorded, 2.0),
    ('stage_17_extension_reply_and_calendar_args_exact', stage_17_extension_reply_and_calendar_args_exact, 1.0),
    ('stage_17_offer_not_accepted', stage_17_offer_not_accepted, 2.0),
]
