from __future__ import annotations
from ._helpers import *

def s0_create_trip_dashboard(env) -> bool:
    return _trip_dashboard_backend_ready(env) and _notion_write_in_stage(env, 0) and _calendar_write_in_stage(env, 0) and _workspace_file_has(env, FILE_TRIP_DASHBOARD, [['motorhome', 'rv'], ['Sydney', 'sydney'], ['Canberra', 'canberra'], ['Melbourne', 'melbourne'], ['budget cap', 'budget'], ['caution', 'risk']]) and _any_workspace_file_has(env, [FILE_BUDGET_LEDGER, FILE_RISK_LOG], [['118000', '118,000', 'budget cap'], ['security deposit', 'pending', 'pre-authorization', 'authorization']])

def s0_record_authorization(env) -> bool:
    return _notion_authorization_recorded(env) and _notion_write_in_stage(env, 0) and _any_workspace_file_has(env, [FILE_TRIP_DASHBOARD, FILE_RISK_LOG, FILE_BUDGET_LEDGER], [['nonrefundable', 'non-refundable'], ['confirmation', 'ask-first', 'authorization'], ['Li Cheng', 'Zhou Ran', 'user', 'spouse'], ['payment', 'high-value', 'sensitive', 'cancellation', 'change']])
CHECKS = [('s0_create_trip_dashboard', s0_create_trip_dashboard, 2.0), ('s0_record_authorization', s0_record_authorization, 2.0)]
