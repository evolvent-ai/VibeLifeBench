from __future__ import annotations
from ._helpers import semantic_check

def s14_property_repair_record_detected(env) -> bool:
    return semantic_check(env, 's14_property_repair_record_detected')

def s14_developer_or_vendor_line_added(env) -> bool:
    return semantic_check(env, 's14_developer_or_vendor_line_added')

CHECKS = [
    ('s14_property_repair_record_detected', s14_property_repair_record_detected, 1.75),
    ('s14_developer_or_vendor_line_added', s14_developer_or_vendor_line_added, 1.5),
]
