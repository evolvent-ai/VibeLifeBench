from ._stage_checks import run_stage


def s10_hotel_mutation_policy(env):
    return run_stage(env, 10)


CHECKS = [("s10_hotel_mutation_policy", s10_hotel_mutation_policy, 2.0)]
