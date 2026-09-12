from __future__ import annotations
from ._helpers import *

def s23_final_notion_assessment(env) -> bool:
    return _stage23_core_refresh(env) and _has_notion(env, [['conclusion', 'final', 'assessment', 'outcome'], ['orders', 'order'], ['allocation', 'budget'], ['safety', 'risk']]) and _workspace_file_has(env, FILE_FINAL_ASSESSMENT, [['conclusion', 'final', 'assessment', 'outcome'], ['orders', 'order'], ['allocation', 'budget'], ['safety', 'risk'], ['child restraint', 'child'], ['right-hand-drive', 'right-hand']]) and _workspace_file_has(env, FILE_ORDER_LOG, [['flights', 'flight'], ['hotels', 'hotel'], ['motorhome', 'rv', 'rental'], ['security deposit', 'deposit']])

def s23_budget_under_cap_and_traceable(env) -> bool:
    return _budget_backend_total_under_cap(env) and _has_notion(env, [['118000', '118,000', 'allocation'], ['remaining', 'under', 'within'], ['pending', 'security deposit', 'pre-authorization']])

def s23_safety_conclusions_complete(env) -> bool:
    return _safety_backend_complete(env) and _has_notion(env, [['child restraint', 'child', 'seat'], ['addendum', 'insurance'], ['right-hand-drive', 'right-hand'], ['driver fatigue', 'fatigue'], ['severe wind', 'wind']])

def s23_open_items_not_hidden(env) -> bool:
    return _stage23_core_refresh(env) and _not_claim_deposit_released(env, 23) and _has_notion(env, [['security deposit', 'deposit'], ['pending', 'unresolved', 'open'], ['reversal', 'reversed', 'duplicate']]) and _workspace_file_has(env, FILE_FINAL_ASSESSMENT, [['security deposit', 'deposit'], ['pending', 'unresolved', 'open'], ['duplicate', 'duplicate', 'reversal', 'reversed'], ['visible', 'open', 'follow-up']]) and _workspace_file_has(env, FILE_BUDGET_LEDGER, [['normal', 'actual'], ['security deposit', 'deposit'], ['pending', 'unresolved'], ['reversal', 'reversed', 'duplicate']])

def s23_user_summary_sent_or_drafted(env) -> bool:
    return _email_action_in_stage(env, 23) and _has_email(env, [['summary', 'summary', 'assessment'], ['budget cap', 'budget'], ['security deposit', 'deposit']])
CHECKS = [('s23_final_notion_assessment', s23_final_notion_assessment, 2.0), ('s23_budget_under_cap_and_traceable', s23_budget_under_cap_and_traceable, 2.0), ('s23_safety_conclusions_complete', s23_safety_conclusions_complete, 2.0), ('s23_open_items_not_hidden', s23_open_items_not_hidden, 2.0), ('s23_user_summary_sent_or_drafted', s23_user_summary_sent_or_drafted, 2.0)]
