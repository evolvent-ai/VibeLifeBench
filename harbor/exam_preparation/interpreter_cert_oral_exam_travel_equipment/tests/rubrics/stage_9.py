from __future__ import annotations

from ._helpers import rule_ok

def s09_travel_options_refundable(env) -> bool:
    return rule_ok(env, 's09_travel_options_refundable')

def s09_travel_search_trace_anchor(env) -> bool:
    return rule_ok(env, 's09_travel_search_trace_anchor')

def s09_no_nonrefundable_booking(env) -> bool:
    return rule_ok(env, 's09_no_nonrefundable_booking')

CHECKS = [
    ('s09_travel_options_refundable', s09_travel_options_refundable, 1.75),
    ('s09_travel_search_trace_anchor', s09_travel_search_trace_anchor, 1.0),
    ('s09_no_nonrefundable_booking', s09_no_nonrefundable_booking, 2.0),
]
