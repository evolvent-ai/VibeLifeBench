from ._stage_checks import run_stage


def s16_executable_plan_and_status(env):
    return run_stage(env, 16)


CHECKS = [("s16_executable_plan_and_status", s16_executable_plan_and_status, 2.0)]
