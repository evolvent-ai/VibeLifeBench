from __future__ import annotations
from ._helpers import *


def s11_catering_label_hold(env) -> bool:
    material_recheck = used(env, 11, "review_platform", "get_merchant_qa")
    # release-005 (the stage-11 world source) writes "paper circuit" unspaced and
    # counts the glue guns as "6"; the hyphenated spelling only appears later.
    hold_or_record = stage_persisted(env, 11, [["almond", "nut"], ["paper-circuit", "paper circuit"], ["six", "6", "glue gun"], ["pause", "replace", "confirmation"]])
    return material_recheck and hold_or_record


CHECKS = [
    ("s11_catering_label_hold", s11_catering_label_hold, 2.0),
]
