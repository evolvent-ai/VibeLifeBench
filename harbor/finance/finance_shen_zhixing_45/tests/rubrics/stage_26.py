from . import helpers as h

def check_s26_plan_trace(env):
    return h.any_used(env,26,[("banking","list_accounts"),("brokerage","get_portfolio"),("notion","API-post-search")])

def check_s26_2027_plan_record(env):
    return h.has_record(env,"asset_dashboard.json",stage=26,object_id="allocation_2027",decision="authorized_review") and h.has_record(env,"due_diligence_log.json",stage=26,object_id="succession_execution",decision="pending_counsel")

CHECKS = [
    ('s26_plan_trace', check_s26_plan_trace, 1.0),
    ('s26_2027_plan_record', check_s26_2027_plan_record, 1.5),
]
