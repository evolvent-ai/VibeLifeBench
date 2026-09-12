from . import helpers as h

def check_s14_inheritance_tools(env):
    return h.any_used(env,14,[("email","search_emails"),("notion","API-post-search"),("calendar","list_events")])

def check_s14_gst_record(env):
    return h.has_record(env,"due_diligence_log.json",stage=14,object_id="gst_life_insurance",decision="pending_counsel") and h.has_record(env,"authorization_log.json",stage=14,object_id="direct_transfer_to_grandson",status="blocked")

CHECKS = [
    ('s14_inheritance_tools', check_s14_inheritance_tools, 1.0),
    ('s14_gst_record', check_s14_gst_record, 1.75),
]
