from ._helpers import neighbor_plan_recorded, trace_stage, text_stage


def s07_neighbor_parking_log(env) -> bool:
    return trace_stage(env, 7) and neighbor_plan_recorded(env)


CHECKS = [
    ("s07_neighbor_parking_log", s07_neighbor_parking_log, 1.2),
]
