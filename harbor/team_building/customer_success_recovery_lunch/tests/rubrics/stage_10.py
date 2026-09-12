from __future__ import annotations
from ._helpers import *

def s10_diagnostic_material_replan(env) -> bool:
    return used(env, 10, 'review_platform', 'get_merchant_qa') and any_write(env, 10) and state_has(env, 10, [['diagnostic', 'assessment'], ['anonymous', 'reflection'], ['changed', 'replace']])

CHECKS = [
    ('s10_diagnostic_material_replan', s10_diagnostic_material_replan, 2.0),
]
