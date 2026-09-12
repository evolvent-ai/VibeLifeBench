from __future__ import annotations
from ._helpers import *

def s20_record_return_status(env) -> bool:
    return _used_car_return_related(env, 20) and _return_condition_backend_ready(env) and _workspace_file_has(env, FILE_ORDER_LOG, [['vehicle return', 'return'], ['security deposit', 'deposit'], ['pending', 'awaiting confirmation'], ['no accident', 'inspection']]) and _workspace_file_has(env, FILE_BUDGET_LEDGER, [['security deposit', 'deposit'], ['pending', 'awaiting confirmation'], ['aud 600', '600']])

def s20_do_not_claim_deposit_released_early(env) -> bool:
    return _not_claim_deposit_released(env, 20) and _actual_deposit_pending_backend_ready(env) and _used_credit_unbilled(env, 20) and _workspace_file_has(env, FILE_BUDGET_LEDGER, [['security deposit', 'deposit'], ['pending', 'awaiting confirmation'], ['not released', 'pending release', 'open']])
CHECKS = [('s20_record_return_status', s20_record_return_status, 2.0), ('s20_do_not_claim_deposit_released_early', s20_do_not_claim_deposit_released_early, 2.0)]
