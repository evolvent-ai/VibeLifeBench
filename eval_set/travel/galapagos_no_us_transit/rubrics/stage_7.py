from ._stage_checks import run_stage


def s7_late_arrival_hotel_safety(env):
    return run_stage(env, 7)


CHECKS = [("s7_late_arrival_hotel_safety", s7_late_arrival_hotel_safety, 2.0)]
