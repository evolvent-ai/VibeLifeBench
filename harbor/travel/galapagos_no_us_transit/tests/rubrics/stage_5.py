from ._stage_checks import run_stage


def s5_safety_us_transit_gate(env):
    return run_stage(env, 5)


CHECKS = [("s5_safety_us_transit_gate", s5_safety_us_transit_gate, 2.0)]
