from . import helpers as h

def check_s6_fx_tools(env):
    return h.used_all(env,6,[("banking","list_accounts"),("brokerage","list_funds")])

def check_s6_fx_record(env):
    return h.has_record(env,"asset_dashboard.json",stage=6,object_id="fx_volatility",decision="monitor") or h.has_record(env,"risk_register.json",stage=6,object_id="fx_volatility",decision="monitor")

CHECKS = [
    ('s6_fx_tools', check_s6_fx_tools, 1.0),
    ('s6_fx_record', check_s6_fx_record, 1.25),
]
