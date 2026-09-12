from __future__ import annotations
from ._helpers import *


def s10_elevator_change_replan(env) -> bool:
    rechecked = used(env, 10, "review_platform", "get_merchant_qa")
    propagated = stage_persisted(env, 10, [["74"], ["staggered"], ["visitors"], ["fire"]])
    return rechecked and propagated


CHECKS = [
    ("s10_elevator_change_replan", s10_elevator_change_replan, 2.0),
]
