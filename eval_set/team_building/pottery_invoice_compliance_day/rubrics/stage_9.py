from ._helpers import evaluate

def s9_route_parking_recheck(env) -> bool:
    return evaluate(env, "s9_route_parking_recheck")

def s9_accessible_waiting_point(env) -> bool:
    return evaluate(env, "s9_accessible_waiting_point")

CHECKS = [
    ("s9_route_parking_recheck", s9_route_parking_recheck, 1.0),
    ("s9_accessible_waiting_point", s9_accessible_waiting_point, 1.0),
]
