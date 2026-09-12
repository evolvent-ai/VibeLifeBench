from ._helpers import *

def s7_scheduled_registration_refresh(env) -> bool:
    return h_s7_scheduled_registration_refresh(env)

def s7_seat_mutation_detected(env) -> bool:
    return h_s7_seat_mutation_detected(env)

CHECKS = [
    ("s7_scheduled_registration_refresh", s7_scheduled_registration_refresh, 1.25),
    ("s7_seat_mutation_detected", s7_seat_mutation_detected, 1.75),
]
