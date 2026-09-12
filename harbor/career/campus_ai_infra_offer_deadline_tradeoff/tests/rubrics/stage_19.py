from __future__ import annotations

from ._helpers import _check


def stage_19_bytelattice_not_counted_and_timeline_risk_recorded(env) -> bool:
    return _check('stage_19_bytelattice_not_counted_and_timeline_risk_recorded', env)


CHECKS = [
    ('stage_19_bytelattice_not_counted_and_timeline_risk_recorded', stage_19_bytelattice_not_counted_and_timeline_risk_recorded, 2.0),
]
