from . import helpers as h

def check_s1_auth_hardcode_trace(env):
    return h.used_all(env,1,[("banking","list_accounts"),("brokerage","get_positions"),("calendar","list_events"),("notion","API-post-search")])

def check_s1_core_backend_and_log(env):
    return h.account_frozen(env,"acct_core_trust") and h.has_record(env,"authorization_log.json",stage=1,object_id="core_sleeve_40pct",status="protected") and h.has_record(env,"asset_dashboard.json",stage=1,object_id="dual_authorization",decision="baseline")

CHECKS = [
    ('s1_auth_hardcode_trace', check_s1_auth_hardcode_trace, 1.25),
    ('s1_core_backend_and_log', check_s1_core_backend_and_log, 2.0),
]
