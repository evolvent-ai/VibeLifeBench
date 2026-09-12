from ._helpers import response_check_id, structured_check_id

def s08_delivery_wrong_item_trace(env) -> bool:
    return structured_check_id(env, 's08_delivery_wrong_item_trace')

def s08_order_status_crosscheck(env) -> bool:
    return structured_check_id(env, 's08_order_status_crosscheck')

CHECKS = [
    ('s08_delivery_wrong_item_trace', s08_delivery_wrong_item_trace, 1.0),
    ('s08_order_status_crosscheck', s08_order_status_crosscheck, 1.0),
]
