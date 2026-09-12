from __future__ import annotations
from ._helpers import *

def s15_account_change_fraud_hold(env) -> bool:
    return used(env, 15, 'email') and any_write(env, 15) and state_has(env, 15, [['personal'], ['non-refundable'], ['hold'], ['verify']])

CHECKS = [
    ('s15_account_change_fraud_hold', s15_account_change_fraud_hold, 2.0),
]
