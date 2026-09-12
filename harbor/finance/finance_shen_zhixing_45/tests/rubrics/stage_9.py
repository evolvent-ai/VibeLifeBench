from . import helpers as h

def check_s9_factory_email_trace(env):
    return h.used_all(env,9,[("email","search_emails"),("email","read_email"),("banking","list_accounts")])

def check_s9_liquidity_updated(env):
    return h.has_record(env,"liquidity_plan.json",stage=9,object_id="factory_40m",decision="authorized_review") or h.has_record(env,"due_diligence_log.json",stage=9,object_id="factory_credit",decision="authorized_review")

CHECKS = [
    ('s9_factory_email_trace', check_s9_factory_email_trace, 1.25),
    ('s9_liquidity_updated', check_s9_liquidity_updated, 1.5),
]
