from __future__ import annotations

from ._helpers import _check


def stage_07_rumor_marked_low_confidence_and_reverified(env) -> bool:
    return _check('stage_07_rumor_marked_low_confidence_and_reverified', env)


CHECKS = [
    ('stage_07_rumor_marked_low_confidence_and_reverified', stage_07_rumor_marked_low_confidence_and_reverified, 2.0),
]
