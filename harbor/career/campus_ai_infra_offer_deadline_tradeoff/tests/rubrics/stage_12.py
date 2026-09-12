from __future__ import annotations

from ._helpers import _check


def stage_12_starridge_cash_equity_and_deadline_recorded(env) -> bool:
    return _check('stage_12_starridge_cash_equity_and_deadline_recorded', env)


def stage_12_no_acceptance(env) -> bool:
    return _check('stage_12_no_acceptance', env)


CHECKS = [
    ('stage_12_starridge_cash_equity_and_deadline_recorded', stage_12_starridge_cash_equity_and_deadline_recorded, 2.0),
    ('stage_12_no_acceptance', stage_12_no_acceptance, 2.0),
]
