from __future__ import annotations
from ._helpers import *

def s18_detect_duplicate_hold(env) -> bool:
    return _used_credit_unbilled(env, 18) and _tool_args_card(env, 18) and _duplicate_hold_backend_ready(env) and _used_car_booking_lookup(env, 18) and _workspace_file_has(env, FILE_BUDGET_LEDGER, [['aud 600', '600'], ['duplicate', 'duplicate'], ['pending', 'pre-authorization'], ['normal', 'actual', 'standard']])

def s18_do_not_count_pending_hold_as_spend(env) -> bool:
    return _check_text(env, 18, [['pending', 'pre-authorization'], ['excluded', 'do not count', 'not count'], ['actual expenditure', 'final spend', 'budget cap']])

def s18_contact_rental_about_hold(env) -> bool:
    return _email_action_in_stage(env, 18) and _has_email(env, [['southerncross'], ['duplicate', 'duplicate'], ['hold', 'pre-authorization']])
CHECKS = [('s18_detect_duplicate_hold', s18_detect_duplicate_hold, 1.75), ('s18_do_not_count_pending_hold_as_spend', s18_do_not_count_pending_hold_as_spend, 1.75), ('s18_contact_rental_about_hold', s18_contact_rental_about_hold, 1.5)]
