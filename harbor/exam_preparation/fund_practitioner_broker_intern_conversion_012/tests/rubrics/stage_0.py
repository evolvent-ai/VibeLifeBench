from ._helpers import *

def s0_hub_created(env) -> bool:
    return h_s0_hub_created(env)

def s0_initial_calendar_plan(env) -> bool:
    return h_s0_initial_calendar_plan(env)

def s0_monitor_subscription(env) -> bool:
    return h_s0_monitor_subscription(env)

CHECKS = [
    ("s0_hub_created", s0_hub_created, 1.25),
    ("s0_initial_calendar_plan", s0_initial_calendar_plan, 1.0),
    ("s0_monitor_subscription", s0_monitor_subscription, 1.0),
]
