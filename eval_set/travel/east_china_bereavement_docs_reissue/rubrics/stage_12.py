from __future__ import annotations
from ._helpers import check_s12_elder_friendly_ningbo_train

def s12_elder_friendly_ningbo_train(env) -> bool:
    return check_s12_elder_friendly_ningbo_train(env)

CHECKS = [
    ("s12_elder_friendly_ningbo_train", s12_elder_friendly_ningbo_train, 3),
]
