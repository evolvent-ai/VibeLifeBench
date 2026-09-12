from ._stage_checks import run_stage


def s4_budget_and_transit_risk(env):
    return run_stage(env, 4)


CHECKS = [("s4_budget_and_transit_risk", s4_budget_and_transit_risk, 2.0)]
