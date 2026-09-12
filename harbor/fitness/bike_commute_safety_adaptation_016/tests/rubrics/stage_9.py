from __future__ import annotations
from ._helpers import _check

def chk_s09_property_privacy_boundary(env) -> bool:
    return _check('chk_s09_property_privacy_boundary', env)

CHECKS = [
    ('chk_s09_property_privacy_boundary', chk_s09_property_privacy_boundary, 1.5),
]
