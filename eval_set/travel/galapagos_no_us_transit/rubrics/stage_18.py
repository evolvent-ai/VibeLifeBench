from ._stage_checks import run_stage


def s18_predeparture_checklist(env):
    return run_stage(env, 18)


CHECKS = [("s18_predeparture_checklist", s18_predeparture_checklist, 2.0)]
