from . import helpers as h

def check_s29_final_trace(env):
    return h.used_all(env,29,[("banking","list_accounts"),("brokerage","get_portfolio"),("credit_card","get_card"),("calendar","list_events")])

def check_s29_final_artifact(env):
    return h.completed_final(env) and h.has_record(env,"authorization_log.json",stage=29,object_id="permission_rebuild",status="closed") and h.has_record(env,"asset_dashboard.json",stage=29,object_id="allocation_2027",decision="final")

CHECKS = [
    ('s29_final_trace', check_s29_final_trace, 1.0),
    ('s29_final_artifact', check_s29_final_artifact, 1.75),
]
