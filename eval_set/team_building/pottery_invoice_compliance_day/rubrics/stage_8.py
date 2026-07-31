from ._helpers import evaluate

def s8_scheduled_monitor_run(env) -> bool:
    return evaluate(env, "s8_scheduled_monitor_run")

def s8_multi_server_refresh(env) -> bool:
    return evaluate(env, "s8_multi_server_refresh")

CHECKS = [
    ("s8_scheduled_monitor_run", s8_scheduled_monitor_run, 1.0),
    ("s8_multi_server_refresh", s8_multi_server_refresh, 1.0),
]
