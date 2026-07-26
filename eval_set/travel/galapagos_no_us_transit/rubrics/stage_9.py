from ._stage_checks import run_stage


def s9_waiver_reliability_choice(env):
    return run_stage(env, 9)


CHECKS = [("s9_waiver_reliability_choice", s9_waiver_reliability_choice, 2.0)]
