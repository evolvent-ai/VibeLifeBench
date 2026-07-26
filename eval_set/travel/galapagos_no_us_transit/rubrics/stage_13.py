from ._stage_checks import run_stage


def s13_seasick_activity_safety(env):
    return run_stage(env, 13)


CHECKS = [("s13_seasick_activity_safety", s13_seasick_activity_safety, 2.0)]
