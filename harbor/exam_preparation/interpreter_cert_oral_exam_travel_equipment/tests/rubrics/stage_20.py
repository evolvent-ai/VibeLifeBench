from __future__ import annotations

from ._helpers import rule_ok

def s20_final_scheduled_refresh(env) -> bool:
    return rule_ok(env, 's20_final_scheduled_refresh')

def s20_open_confirmations_compiled(env) -> bool:
    return rule_ok(env, 's20_open_confirmations_compiled')

def s20_final_refresh_trace_matrix(env) -> bool:
    return rule_ok(env, 's20_final_refresh_trace_matrix')

def s20_multi_service_trace_anchor(env) -> bool:
    return rule_ok(env, 's20_multi_service_trace_anchor')

CHECKS = [
    ('s20_final_scheduled_refresh', s20_final_scheduled_refresh, 1.75),
    ('s20_open_confirmations_compiled', s20_open_confirmations_compiled, 1.5),
    ('s20_final_refresh_trace_matrix', s20_final_refresh_trace_matrix, 1.0),
    ('s20_multi_service_trace_anchor', s20_multi_service_trace_anchor, 1.0),
]
