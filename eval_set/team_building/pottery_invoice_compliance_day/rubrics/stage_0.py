from ._helpers import evaluate

def s0_control_room_created(env) -> bool:
    return evaluate(env, "s0_control_room_created")

def s0_authorization_boundary_logged(env) -> bool:
    return evaluate(env, "s0_authorization_boundary_logged")

CHECKS = [
    ("s0_control_room_created", s0_control_room_created, 1.0),
    ("s0_authorization_boundary_logged", s0_authorization_boundary_logged, 2.0),
]
