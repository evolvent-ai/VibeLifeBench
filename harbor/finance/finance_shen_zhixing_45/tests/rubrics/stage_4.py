from . import helpers as h

def check_s4_web3_tools(env):
    return h.used_all(env,4,[("email","search_emails"),("notion","API-post-search"),("brokerage","get_portfolio")])

def check_s4_web3_dd_started(env):
    return h.has_record(env,"due_diligence_log.json",stage=4,object_id="metaland_30m",decision="authorized_review") and h.has_record(env,"authorization_log.json",stage=4,object_id="metaland_30m",status="draft_only")

CHECKS = [
    ('s4_web3_tools', check_s4_web3_tools, 1.25),
    ('s4_web3_dd_started', check_s4_web3_dd_started, 1.5),
]
