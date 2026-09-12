from __future__ import annotations
from ._helpers import _check

def chk_s22_light_install_check(env) -> bool:
    return _check('chk_s22_light_install_check', env)

CHECKS = [
    ('chk_s22_light_install_check', chk_s22_light_install_check, 1.25),
]
