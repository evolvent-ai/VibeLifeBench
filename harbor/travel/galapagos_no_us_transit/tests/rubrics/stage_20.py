from ._stage_checks import run_stage


def s20_in_transit_arrival_sync(env):
    return run_stage(env, 20)


CHECKS = [("s20_in_transit_arrival_sync", s20_in_transit_arrival_sync, 2.0)]
