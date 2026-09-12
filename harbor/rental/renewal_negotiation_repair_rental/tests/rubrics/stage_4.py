from __future__ import annotations
from ._helpers import *

def s4_repair_review_sources(env) -> bool:
    return bool(
        tool_stage_object(env, 4, 'review_platform', None, C.MER_A, ('Qinghe Jiayuan',))
        and tool_stage_object(env, 4, 'review_platform', None, C.MER_C, ('Qinghe Alternative Residence',))
        and review_has(env, C.MER_A, ('wall dampness', 'water heater'))
        and review_has(env, C.MER_C, ('nighttime', 'residence registration'))
    )

def s4_risk_page_update(env) -> bool:
    return bool(
        review_has(env, C.MER_A, ('wall dampness',))
        and derived_stage_has(env, 4, (C.LIST_A, 'seepage', 'repair', 'evidence_source'), ('RISK_LOG.md', 'LEASE_CHECKLIST.md'))
    )

CHECKS = [
    ("s4_repair_review_sources", s4_repair_review_sources, 1.5),
    ("s4_risk_page_update", s4_risk_page_update, 1.25),
]
