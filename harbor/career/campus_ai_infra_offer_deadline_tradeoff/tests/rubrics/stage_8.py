from __future__ import annotations

from ._helpers import _check


def stage_08_starridge_status_and_quiet_tracker_updated(env) -> bool:
    return _check('stage_08_starridge_status_and_quiet_tracker_updated', env)


CHECKS = [
    ('stage_08_starridge_status_and_quiet_tracker_updated', stage_08_starridge_status_and_quiet_tracker_updated, 2.0),
]
