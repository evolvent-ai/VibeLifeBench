from ._helpers import *


def s1_required_servers_touched(env):
    return all_required_servers_used(env, stage=1)


def s1_object_index_target(env):
    return (
        doc_value(env, 'object_index.json', 'order_id', ORDER_ID)
        and doc_value(env, 'object_index.json', 'tracking_no', TRACKING_NO)
        and record_has(env, 'object_index.json', 'places', 'place_id', MERCHANT_PLACE)
        and delivery_target_identity_matches(env)
        and maps_place_checked(env, MERCHANT_PLACE)
    )


CHECKS = [('s1_required_servers_touched', s1_required_servers_touched, 1.5), ('s1_object_index_target', s1_object_index_target, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
