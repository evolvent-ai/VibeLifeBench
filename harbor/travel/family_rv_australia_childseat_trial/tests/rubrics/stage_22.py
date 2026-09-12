from __future__ import annotations
from ._helpers import *

def s22_update_hold_reversal(env) -> bool:
    return _used_credit_unbilled(env, 22) and _tool_args_card(env, 22) and _duplicate_hold_reversal_backend_ready(env) and _workspace_file_has(env, FILE_BUDGET_LEDGER, [['reversal', 'reversed', 'reversed'], ['duplicate', 'duplicate'], ['600'], ['pending', 'pre-authorization']])

def s22_keep_actual_deposit_pending(env) -> bool:
    return _used_credit_unbilled(env, 22) and _actual_deposit_pending_backend_ready(env) and _workspace_file_has(env, FILE_BUDGET_LEDGER, [['normal', 'actual'], ['security deposit', 'deposit'], ['pending', 'pending release'], ['600']])
CHECKS = [('s22_update_hold_reversal', s22_update_hold_reversal, 2.0), ('s22_keep_actual_deposit_pending', s22_keep_actual_deposit_pending, 1.5)]
