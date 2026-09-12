from __future__ import annotations

from ._helpers import rule_ok

def s19_center_change_replan(env) -> bool:
    return rule_ok(env, 's19_center_change_replan')

def s19_center_change_trace_replan(env) -> bool:
    return rule_ok(env, 's19_center_change_trace_replan')

def s19_center_notice_map_anchor(env) -> bool:
    return rule_ok(env, 's19_center_notice_map_anchor')

CHECKS = [
    ('s19_center_change_replan', s19_center_change_replan, 2.0),
    ('s19_center_change_trace_replan', s19_center_change_trace_replan, 1.0),
    ('s19_center_notice_map_anchor', s19_center_notice_map_anchor, 1.0),
]
