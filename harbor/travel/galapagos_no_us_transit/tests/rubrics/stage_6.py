from ._stage_checks import run_stage


def s6_flight_mutation_hold(env):
    return run_stage(env, 6)


CHECKS = [("s6_flight_mutation_hold", s6_flight_mutation_hold, 2.0)]
