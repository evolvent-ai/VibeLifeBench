from __future__ import annotations

from ._helpers import _check


def stage_11_matrixcloud_cash_and_onsite_detected(env) -> bool:
    return _check('stage_11_matrixcloud_cash_and_onsite_detected', env)


def stage_11_matrixcloud_not_recommended_as_compliant(env) -> bool:
    return _check('stage_11_matrixcloud_not_recommended_as_compliant', env)


def stage_11_no_offer_rejection(env) -> bool:
    return _check('stage_11_no_offer_rejection', env)


CHECKS = [
    ('stage_11_matrixcloud_cash_and_onsite_detected', stage_11_matrixcloud_cash_and_onsite_detected, 1.75),
    ('stage_11_matrixcloud_not_recommended_as_compliant', stage_11_matrixcloud_not_recommended_as_compliant, 2.0),
    ('stage_11_no_offer_rejection', stage_11_no_offer_rejection, 2.0),
]
