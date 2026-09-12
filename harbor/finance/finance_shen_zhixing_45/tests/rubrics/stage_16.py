from . import helpers as h

def check_s16_shops_trace(env):
    return h.used_all(env,16,[("notion","API-post-search"),("notion","API-get-block-children"),("banking","list_accounts")])

def check_s16_fire_sale_block(env):
    return h.has_record(env,"authorization_log.json",stage=16,object_id="core_shops_fire_sale",status="blocked") and h.has_record(env,"asset_dashboard.json",stage=16,object_id="rent_yield_spread",decision="protected")

CHECKS = [
    ('s16_shops_trace', check_s16_shops_trace, 1.0),
    ('s16_fire_sale_block', check_s16_fire_sale_block, 1.75),
]
