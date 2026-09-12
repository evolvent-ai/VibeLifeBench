from ._helpers import response_check_id, structured_check_id

def s06_material_product_filter(env) -> bool:
    return structured_check_id(env, 's06_material_product_filter')

def s06_publisher_notice_crosscheck(env) -> bool:
    return structured_check_id(env, 's06_publisher_notice_crosscheck')

CHECKS = [
    ('s06_material_product_filter', s06_material_product_filter, 1.0),
    ('s06_publisher_notice_crosscheck', s06_publisher_notice_crosscheck, 1.0),
]
