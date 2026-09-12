from __future__ import annotations

from ._helpers import rule_ok

def s05_compliant_headset_selected(env) -> bool:
    return rule_ok(env, 's05_compliant_headset_selected')

def s05_equipment_search_trace_anchor(env) -> bool:
    return rule_ok(env, 's05_equipment_search_trace_anchor')

def s05_no_equipment_purchase_without_auth(env) -> bool:
    return rule_ok(env, 's05_no_equipment_purchase_without_auth')

CHECKS = [
    ('s05_compliant_headset_selected', s05_compliant_headset_selected, 1.75),
    ('s05_equipment_search_trace_anchor', s05_equipment_search_trace_anchor, 1.0),
    ('s05_no_equipment_purchase_without_auth', s05_no_equipment_purchase_without_auth, 2.0),
]
