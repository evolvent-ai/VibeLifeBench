from ._stage_checks import run_stage


def s19_departure_delay_response(env):
    return run_stage(env, 19)


CHECKS = [("s19_departure_delay_response", s19_departure_delay_response, 2.0)]
