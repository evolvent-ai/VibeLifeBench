from ._stage_checks import run_stage


def s24_final_archive(env):
    return run_stage(env, 24)


CHECKS = [("s24_final_archive", s24_final_archive, 3.0)]
