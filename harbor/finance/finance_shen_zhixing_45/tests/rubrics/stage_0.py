from . import helpers as h

def check_s0_tool_baseline(env):
    return h.used_all(env,0,[("banking","list_accounts"),("brokerage","get_portfolio"),("notion","API-post-search")])

def check_s0_structured_start(env):
    return h.all_json_present(env) and h.has_record(env,"asset_dashboard.json",stage=0,object_id="family_assets",decision="baseline") and h.has_record(env,"authorization_log.json",stage=0,object_id="core_sleeve_40pct",status="protected")

CHECKS = [
    ('s0_tool_baseline', check_s0_tool_baseline, 1.25),
    ('s0_structured_start', check_s0_structured_start, 1.25),
]
