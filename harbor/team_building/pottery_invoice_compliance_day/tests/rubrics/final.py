from ._helpers import evaluate


def final_report_cross_services(env) -> bool:
    return evaluate(env, "final_report_cross_services")


def final_open_items_present(env) -> bool:
    return evaluate(env, "final_open_items_present")


CHECKS = [
    ("final_report_cross_services", final_report_cross_services, 6.0),
    ("final_open_items_present", final_open_items_present, 6.0),
]
