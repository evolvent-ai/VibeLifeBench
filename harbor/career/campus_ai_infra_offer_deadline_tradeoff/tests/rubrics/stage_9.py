from __future__ import annotations

from ._helpers import _check


def stage_09_summary_distinguishes_status_and_confirmations(env) -> bool:
    return _check('stage_09_summary_distinguishes_status_and_confirmations', env)


CHECKS = [
    ('stage_09_summary_distinguishes_status_and_confirmations', stage_09_summary_distinguishes_status_and_confirmations, 1.5),
]
