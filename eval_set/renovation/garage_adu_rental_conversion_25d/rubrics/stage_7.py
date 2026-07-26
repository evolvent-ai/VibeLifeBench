from ._helpers import trace_stage, text_stage


def s07_neighbor_parking_log(env) -> bool:
    return trace_stage(env, 7) and text_stage(env, 7, [["neighbor", "邻居"], ["parking", "停车"], ["access", "通行"], ["noise", "噪音"]])


CHECKS = [
    ("s07_neighbor_parking_log", s07_neighbor_parking_log, 1.2),
]
