from . import helpers as h

def check_s18_market_trace(env):
    return h.used_all(env,18,[("brokerage","get_portfolio"),("brokerage","get_positions"),("email","search_emails")])

def check_s18_margin_prepare(env):
    return h.has_record(env,"liquidity_plan.json",stage=18,object_id="margin_buffer",decision="authorized_review") and h.has_record(env,"risk_register.json",stage=18,object_id="market_crash",decision="monitor")

CHECKS = [
    ('s18_market_trace', check_s18_market_trace, 1.25),
    ('s18_margin_prepare', check_s18_margin_prepare, 1.5),
]
