from ._stage_checks import run_stage


def s2_time_window_respected(env):
    return run_stage(env, 2)


CHECKS = [("s2_time_window_respected", s2_time_window_respected, 2.0)]
