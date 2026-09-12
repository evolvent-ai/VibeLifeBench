from ._helpers import response_check_id, structured_check_id

def s19_delivery_exception_issue(env) -> bool:
    return structured_check_id(env, 's19_delivery_exception_issue')

def s19_delivery_status_subscription(env) -> bool:
    return structured_check_id(env, 's19_delivery_status_subscription')

CHECKS = [
    ('s19_delivery_exception_issue', s19_delivery_exception_issue, 1.0),
    ('s19_delivery_status_subscription', s19_delivery_status_subscription, 1.0),
]
