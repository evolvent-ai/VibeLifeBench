from ._stage_checks import run_stage


def s11_authorized_holds(env):
    return run_stage(env, 11)


CHECKS = [("s11_authorized_holds", s11_authorized_holds, 2.0)]
