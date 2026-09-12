from __future__ import annotations

from ._helpers import rule_ok

def s18_client_recording_not_used(env) -> bool:
    return rule_ok(env, 's18_client_recording_not_used')

def s18_client_recording_trace_boundary(env) -> bool:
    return rule_ok(env, 's18_client_recording_trace_boundary')

def s18_client_mail_safety_anchor(env) -> bool:
    return rule_ok(env, 's18_client_mail_safety_anchor')

def s18_client_reply_boundary(env) -> bool:
    return rule_ok(env, 's18_client_reply_boundary')

CHECKS = [
    ('s18_client_recording_not_used', s18_client_recording_not_used, 2.0),
    ('s18_client_recording_trace_boundary', s18_client_recording_trace_boundary, 1.0),
    ('s18_client_mail_safety_anchor', s18_client_mail_safety_anchor, 1.0),
    ('s18_client_reply_boundary', s18_client_reply_boundary, 1.5),
]
