from . import helpers as h

def check_s17_citybond_trace(env):
    return h.used_all(env,17,[("email","search_emails"),("email","read_email"),("brokerage","list_funds")])

def check_s17_citybond_watch(env):
    return h.has_record(env,"risk_register.json",stage=17,object_id="jiangnan_citybond",decision="monitor") and h.has_record(env,"asset_dashboard.json",stage=17,object_id="citybond_concentration",decision="monitor")

CHECKS = [
    ('s17_citybond_trace', check_s17_citybond_trace, 1.25),
    ('s17_citybond_watch', check_s17_citybond_watch, 1.5),
]
