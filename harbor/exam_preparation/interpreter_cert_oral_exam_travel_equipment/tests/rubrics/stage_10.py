from __future__ import annotations

from ._helpers import rule_ok

def s10_time_change_official_refresh(env) -> bool:
    return rule_ok(env, 's10_time_change_official_refresh')

def s10_time_change_trace_refresh(env) -> bool:
    return rule_ok(env, 's10_time_change_trace_refresh')

def s10_official_time_mail_anchor(env) -> bool:
    return rule_ok(env, 's10_official_time_mail_anchor')

def s10_calendar_travel_updated(env) -> bool:
    return rule_ok(env, 's10_calendar_travel_updated')

CHECKS = [
    ('s10_time_change_official_refresh', s10_time_change_official_refresh, 2.0),
    ('s10_time_change_trace_refresh', s10_time_change_trace_refresh, 1.0),
    ('s10_official_time_mail_anchor', s10_official_time_mail_anchor, 1.0),
    ('s10_calendar_travel_updated', s10_calendar_travel_updated, 1.5),
]
