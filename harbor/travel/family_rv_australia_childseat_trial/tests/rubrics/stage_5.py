from __future__ import annotations
from ._helpers import *

def s5_detect_childseat_stock_change(env) -> bool:
    return _used_car_offer_lookup(env, 5) and _southerncross_offer_stock_is_one(env) and _check_text(env, 5, [['child', 'child restraint'], ['1', 'one', 'inventory'], ['cancellable', 'refundable']])

def s5_email_childseat_standard_query(env) -> bool:
    return _email_action_in_stage(env, 5) and _has_email(env, [['child', 'child restraint'], ['as/nzs', 'compliant', 'approved']])

def s5_update_risk_log(env) -> bool:
    return _used_car_offer_lookup(env, 5) and _tool_args_southerncross_offer(env, 5) and _southerncross_offer_stock_is_one(env) and _workspace_file_has(env, FILE_RISK_LOG, [['caution', 'risk'], ['child restraint', 'child'], ['inventory', 'qty', '1', 'one'], ['as/nzs', 'approved', 'compliant']])
CHECKS = [('s5_detect_childseat_stock_change', s5_detect_childseat_stock_change, 1.75), ('s5_email_childseat_standard_query', s5_email_childseat_standard_query, 1.5), ('s5_update_risk_log', s5_update_risk_log, 1.5)]
