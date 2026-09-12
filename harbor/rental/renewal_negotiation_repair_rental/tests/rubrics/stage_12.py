from __future__ import annotations
from ._helpers import *

def s12_water_complaint_recovered(env) -> bool:
    return bool(
        tool_stage_object(env, 12, 'review_platform', None, C.MER_A, ('Qinghe Jiayuan',))
        and tool_stage_object(env, 12, 'maps', None, C.PLACE_A, ('Qinghe Jiayuan',))
        and review_has(env, C.MER_A, ('2026-07-24', 'exterior wall joint', 'responsible party'))
        and place_has_parts(env, C.PLACE_A, ('Qinghe Jiayuan',))
        and derived_stage_has(env, 12, (C.LIST_A, 'seepage', 'exterior wall joint', 'pending confirmation'), ('RISK_LOG.md', 'LEASE_CHECKLIST.md'))
    )

def s12_safety_risk_escalated(env) -> bool:
    return bool(
        tool_stage_object(env, 12, 'review_platform', None, C.MER_B, ('Yongtaizhuang North Road',))
        and tool_stage_object(env, 12, 'maps', None, C.PLACE_B, ('Yongtaizhuang North Road',))
        and review_has(env, C.MER_B, ('23:30', 'west gate'))
        and place_has_parts(env, C.PLACE_B, ('late_night_west_gate_detour',))
        and positive_authorization_boundary(env, 12, ('privately', 'payment'))
    )

CHECKS = [
    ("s12_water_complaint_recovered", s12_water_complaint_recovered, 1.75),
    ("s12_safety_risk_escalated", s12_safety_risk_escalated, 2.0),
]
