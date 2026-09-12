from ._stage_checks import run_stage


def s0_bootstrap_state(env):
    return run_stage(env, 0)


CHECKS = [("s0_bootstrap_state", s0_bootstrap_state, 2.0)]
