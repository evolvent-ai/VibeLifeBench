from ._helpers import evaluate

def s19_onsite_minimized_notice(env) -> bool:
    return evaluate(env, "s19_onsite_minimized_notice")

def s19_workpiece_label_guard(env) -> bool:
    return evaluate(env, "s19_workpiece_label_guard")

CHECKS = [
    ("s19_onsite_minimized_notice", s19_onsite_minimized_notice, 1.0),
    ("s19_workpiece_label_guard", s19_workpiece_label_guard, 1.0),
]
