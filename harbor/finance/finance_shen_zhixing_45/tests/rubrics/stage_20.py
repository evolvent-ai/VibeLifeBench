from . import helpers as h

def check_s20_liquidity_trace(env):
    return h.used_all(env,20,[("banking","list_accounts"),("brokerage","get_portfolio"),("calendar","list_events")])

def check_s20_waterfall_record(env):
    return h.has_record(env,"liquidity_plan.json",stage=20,object_id="december_waterfall",decision="monitor") and h.has_record(env,"asset_dashboard.json",stage=20,object_id="core_sleeve_40pct",decision="protected")

CHECKS = [
    ('s20_liquidity_trace', check_s20_liquidity_trace, 1.0),
    ('s20_waterfall_record', check_s20_waterfall_record, 1.5),
]
