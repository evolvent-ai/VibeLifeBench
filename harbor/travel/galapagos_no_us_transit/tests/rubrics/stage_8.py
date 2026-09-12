from ._stage_checks import run_stage


def s8_ash_disruption_replan(env):
    return run_stage(env, 8)


CHECKS = [("s8_ash_disruption_replan", s8_ash_disruption_replan, 2.0)]
