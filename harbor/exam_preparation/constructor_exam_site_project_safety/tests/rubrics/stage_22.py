from ._helpers import response_check_id, structured_check_id

def s22_final_official_refresh(env) -> bool:
    return structured_check_id(env, 's22_final_official_refresh')

def s22_weather_route_refresh(env) -> bool:
    return structured_check_id(env, 's22_weather_route_refresh')

CHECKS = [
    ('s22_final_official_refresh', s22_final_official_refresh, 1.0),
    ('s22_weather_route_refresh', s22_weather_route_refresh, 1.0),
]
