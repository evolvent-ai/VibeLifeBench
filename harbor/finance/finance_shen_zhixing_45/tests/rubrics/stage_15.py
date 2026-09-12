from . import helpers as h

def check_s15_property_tools(env):
    return h.used_all(env,15,[("notion","API-post-search"),("notion","API-get-block-children")])

def check_s15_yield_model_record(env):
    return h.has_record(env,"asset_dashboard.json",stage=15,object_id="core_retail_properties",decision="monitor") or h.has_record(env,"due_diligence_log.json",stage=15,object_id="rent_yield_spread",decision="authorized_review")

CHECKS = [
    ('s15_property_tools', check_s15_property_tools, 1.0),
    ('s15_yield_model_record', check_s15_yield_model_record, 1.25),
]
