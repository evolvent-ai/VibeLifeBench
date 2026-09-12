from . import helpers as h

def check_s25_calendar_trace(env):
    return h.any_used(env,25,[("calendar","create_event"),("calendar","list_events"),("notion","API-post-search")])

def check_s25_meeting_pack(env):
    return h.has_record(env,"due_diligence_log.json",stage=25,object_id="family_meeting_pack",decision="authorized_review") or h.has_record(env,"asset_dashboard.json",stage=25,object_id="family_meeting_pack",decision="authorized_review")

CHECKS = [
    ('s25_calendar_trace', check_s25_calendar_trace, 1.25),
    ('s25_meeting_pack', check_s25_meeting_pack, 1.25),
]
