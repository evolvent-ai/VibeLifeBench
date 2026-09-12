from ._helpers import response_check_id, structured_check_id

def s16_route_disruption_refresh(env) -> bool:
    return structured_check_id(env, 's16_route_disruption_refresh')

def s16_rail_offer_compare(env) -> bool:
    return structured_check_id(env, 's16_rail_offer_compare')

CHECKS = [
    ('s16_route_disruption_refresh', s16_route_disruption_refresh, 1.0),
    ('s16_rail_offer_compare', s16_rail_offer_compare, 1.0),
]
