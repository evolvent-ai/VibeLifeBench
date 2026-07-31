from ._stage_checks import run_stage


def s12_name_match_scope(env):
    return run_stage(env, 12)


CHECKS = [("s12_name_match_scope", s12_name_match_scope, 2.0)]
