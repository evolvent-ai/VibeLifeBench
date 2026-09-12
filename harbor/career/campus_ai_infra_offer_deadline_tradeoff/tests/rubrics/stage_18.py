from __future__ import annotations

from ._helpers import _check


def stage_18_evidence_confidence_updated_without_overclaim(env) -> bool:
    return _check('stage_18_evidence_confidence_updated_without_overclaim', env)


CHECKS = [
    ('stage_18_evidence_confidence_updated_without_overclaim', stage_18_evidence_confidence_updated_without_overclaim, 2.0),
]
