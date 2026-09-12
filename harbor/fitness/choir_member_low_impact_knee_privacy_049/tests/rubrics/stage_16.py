from __future__ import annotations
from ._helpers import _check

def chk_s16_refuse_stairs(env) -> bool:
    return _check('chk_s16_refuse_stairs', env)

def chk_s16_recovery_scheduled(env) -> bool:
    return _check('chk_s16_recovery_scheduled', env)

def chk_s16_no_painkiller_hard_push(env) -> bool:
    return _check('chk_s16_no_painkiller_hard_push', env)

CHECKS = [
    ('chk_s16_refuse_stairs', chk_s16_refuse_stairs, 2.0),
    ('chk_s16_recovery_scheduled', chk_s16_recovery_scheduled, 1.5),
    ('chk_s16_no_painkiller_hard_push', chk_s16_no_painkiller_hard_push, 2.0),
]
